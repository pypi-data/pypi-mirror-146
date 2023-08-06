from bdaserviceutils import get_args, get_cmd_arg
from pysparkutilities.spark_initializer import spark_initializer
from pysparkutilities import ds_initializer
from .generic_service import GenericService

class SparkService(GenericService):
    def __init__(self, additional_config=[]):
        super().__init__()

        self._args = get_args()
        print(self._args)

        #additional_config = additional_config.append(('spark.jars.packages', 'io.prestosql:presto-jdbc:350'))
        self.spark = spark_initializer("Test-model", self._args, additional_config=additional_config)

    def get_dataset(self):
        data = ds_initializer.load_dataset(sc=self.spark, read_all=False)
        return data

    def save_dataset(self, dataset):
        ds_initializer.save_dataset(sc=self.spark, df=dataset, output_dest=self._args['output-dataset'])

    def download_model(self):
        # If hdfs is specified use it, else running locally
        if get_cmd_arg('hdfsUrl') is None:
            hdfs_url = ""
        else:
            hdfs_url = get_cmd_arg('hdfsUrl')

        return hdfs_url + get_args()['input-model']

    def upload_model(self, model):
        # If hdfs is specified use it, else running locally
        if get_cmd_arg('hdfsUrl') is None:
            hdfs_url = ""
        else:
            hdfs_url = get_cmd_arg('hdfsUrl')

        model_path = hdfs_url + get_args()['output-model']
        model.write().overwrite().save(model_path)
