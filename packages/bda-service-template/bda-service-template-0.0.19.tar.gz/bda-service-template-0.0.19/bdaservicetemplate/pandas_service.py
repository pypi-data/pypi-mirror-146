from .spark_service import SparkService
import pandas as pd
import os
import glob
from fileioutilities.file_io import FileIO
from bdaserviceutils import get_args

def from_spark_to_pandas_df_using_disk(df, path='/tmp/tmp_csv_df'):

    df = df.to_pandas_on_spark()
    df.to_csv(path, header=True, num_files=1, mode="overwrite")

    extension = 'csv'
    os.chdir(path)
    result = glob.glob('*.{}'.format(extension))[0]

    return pd.read_csv(result)


class PandasService(SparkService):
    def __init__(self):
        super().__init__()

    def get_dataset(self):
        df = super().get_dataset() #.toPandas()
        return from_spark_to_pandas_df_using_disk(df)

    def save_dataset(self, dataset):
        super().save_dataset(self.spark.createDataFrame(dataset))

    def download_model(self):

        path = os.path.join(".", "model")
        fileIO = FileIO(storage_type=self._args['dataStorageType-input-model'])
        fileIO.download(remote_path=get_args()['input-model'], local_path=path)
        return path

    def upload_model(self, path):

        fileIO = FileIO(storage_type=self._args['dataStorageType-output-model'])
        fileIO.upload(local_path=path, remote_path=self._args['output-model'])
