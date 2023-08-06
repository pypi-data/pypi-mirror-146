import numpy as np
import hicstraw as hs
import pandas as pd
import sys

import tensorflow as tf

print("hic-straw", hs.__version__)
FEATURE_KEY = 'feat_resolution'
CHROM_KEY = 'chr1'
X1_KEY = 'x1'
X2_KEY = 'x2'
Y1_KEY = 'y1'
Y2_KEY = 'y2'


def find_resolutions_from_list(df):
    df[FEATURE_KEY] = df[X2_KEY] - df[X1_KEY]
    print('Feature list contains the following resolutions:', df[FEATURE_KEY].unique())
    return df[FEATURE_KEY].unique()


def make_resolution_sub_lists(df):
    if '#chr1' in df.columns:
        df.rename(columns={'#chr1': CHROM_KEY}, inplace=True)
    df = df.sort_values(FEATURE_KEY)
    groups = df.groupby(FEATURE_KEY)
    dct = {name: group for name, group in groups}
    return dct


def round_by_res(value, resolution):
    return (value // resolution) * resolution


def make_region(coordinates, width: int, resolution: int):
    (chrom1, x1, x2, y1, y2) = coordinates
    mid_x = round_by_res(x1 + ((x2 - x1) // 2), resolution)
    mid_y = round_by_res(y1 + ((y2 - y1) // 2), resolution)

    half_width = (width // 2) * resolution
    cx1 = mid_x - half_width
    cx2 = mid_x + half_width
    cy1 = mid_y - half_width
    cy2 = mid_y + half_width
    return cx1, cx2, cy1, cy2


class Oracle:
    def __init__(self, loop_list_path: str, hic_file: str, models_dir: str, norm: str, width: int = 56):
        self.__loopList = self.load_loops(loop_list_path)
        self.__hic = hs.HiCFile(hic_file)
        self.__norm = norm
        self.__width = width
        self.__modelsDir = models_dir
        self.__resolutions = sorted(find_resolutions_from_list(self.__loopList))
        self.__resolution_sub_lists = make_resolution_sub_lists(self.__loopList)
        self.__chr = [x.name for x in self.__hic.getChromosomes() if x.name != 'All']

    @staticmethod
    def load_loops(loop_list):
        df = pd.read_csv(loop_list, sep="\t")
        if '#chr1' in df.columns:
            df.rename(columns={'#chr1': CHROM_KEY}, inplace=True)
        # df = df[~df['#chr1'].str.contains("#")]
        df = df.astype({X1_KEY: int, X2_KEY: int, Y1_KEY: int, Y2_KEY: int})
        return df

    @staticmethod
    def preprocess(matrix, scale=0.1):
        if np.sum(matrix) < 1e-9:
            return matrix
        flattened_data = matrix.flatten()
        flattened_data = flattened_data[flattened_data > 0]
        median_val = np.median(flattened_data)
        mad_val = np.median(np.abs(flattened_data - median_val))
        if mad_val == 0:
            return matrix
        m = np.tanh(scale * (matrix - median_val) / mad_val)
        return (m - m.min()) / (m.max() - m.min())

    def run(self):
        model = tf.keras.models.load_model(self.__modelsDir)
        mzd_dict = {
            res: {x: self.__hic.getMatrixZoomData(x, x, "observed", self.__norm, "BP", res) for x in self.__chr} for
            res in self.__resolutions}
        passed = []
        failed = []

        print('Feature list contains the following resolutions:', self.__resolutions)

        # todo should run one chromosome at a time
        # load just the matrix zoom data for that chromosome at that resolution
        # handle all the loops on that chromosome in the batch
        # will save on RAM, and for very large lists, will be important
        # especially the diff loop scenario

        for res, sublist in self.__resolution_sub_lists.items():
            print('ORACLE is running at', res, 'kb')

            if len(failed) > 0:
                failed.drop(['prediction'], axis=1, inplace=True)
                sublist = pd.concat([sublist, failed], ignore_index=True)
            sublist = sublist.reset_index(drop=True)
            batch = np.zeros((len(sublist), self.__width, self.__width, 1))

            for index, row in sublist.iterrows():
                x1, x2, y1, y2 = make_region((row[CHROM_KEY], row[X1_KEY], row[X2_KEY], row[Y1_KEY], row[Y2_KEY]),
                                             self.__width - 1, res)
                # mz = self.__hic.getMatrixZoomData(row[CHROM_KEY], row[CHROM_KEY], "observed", self.__norm , "BP", res)
                mat = mzd_dict[res][row[CHROM_KEY]].getRecordsAsMatrix(x1, x2, y1, y2)
                batch[index, :self.__width - 1, :self.__width - 1, 0] = self.preprocess(mat)
            prediction = model.predict(batch)
            sublist['prediction'] = prediction
            passed.append(sublist[sublist['prediction'] >= 0.5])
            failed = sublist[sublist['prediction'] < 0.5]

        return pd.concat(passed, ignore_index=True), failed


# python3 oracle.py <file.hic> </dir/models> </dir/bedpe> <norm>

if __name__ == "__main__":
    FILEPATH = sys.argv[1]
    MODEL_DIR = sys.argv[2]
    BEDPE_DIR = sys.argv[3]
    NORMALIZATION_TYPE = sys.argv[4]

    oracle = Oracle(BEDPE_DIR, FILEPATH, MODEL_DIR, NORMALIZATION_TYPE)
    passing, failing = oracle.run()

    print('Saving results to disk...')

    filename = BEDPE_DIR.split('/')[-1].replace('.bedpe', "")

    passing.to_csv(filename + '_ORACLE_passed.bedpe', sep="\t", index=False)
    failing.to_csv(filename + '_ORACLE_failed.bedpe', sep="\t", index=False)

    print('Done.')
