from abc import ABC

# from pyspark.sql import SparkSession
#
# from sparkle_session import session_sparkle
from pyspark.sql import SparkSession

from sparkle_session.session import session_sparkle


class SparkAndLog(ABC):
    """
    Add a Spark session and a Logger to your class
    """
    log_level = "INFO"

    def __init__(self):
        self.spark = session_sparkle(SparkSession.builder.getOrCreate())
        self.log = self.spark.log(log_level=self.log_level)
        self.logging = self.log
        self.logger = self.log
