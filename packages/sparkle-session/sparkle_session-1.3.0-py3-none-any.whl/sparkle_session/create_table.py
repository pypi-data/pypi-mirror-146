from abc import ABC, abstractmethod

import re
from pyspark.sql.types import StructType
from typing import List

from sparkle_session.spark_and_log import SparkAndLog

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS {} ({}) LOCATION 'THELOC' PARTS STORED AS PARQUET"


class SQLResolver(ABC):

    @abstractmethod
    def resolve(self, in_sql: str):
        pass


class ResolverPipeline(SQLResolver):

    def __init__(self, stages: List[SQLResolver]):
        self.stages = stages

    def resolve(self, in_sql: str):
        sql = in_sql
        for s in self.stages:
            sql = s.resolve(sql)
        return sql


class PartitionSQL(SQLResolver):
    def __init__(self, partition_cols: StructType = None):
        self.partition_cols = partition_cols

    def resolve(self, in_sql: str):
        return in_sql.replace('PARTS', self._partitioning())

    def _partitioning(self):
        if self.partition_cols:
            to_str = [f.name + " " + f.dataType.simpleString() for f in self.partition_cols.fields]
            return "PARTITIONED BY ({})".format(", ".join(to_str))
        else:
            return ""


class LocationSQL(SQLResolver):
    def __init__(self, location: str = None):
        self.location = location

    def resolve(self, in_sql: str):
        if not self.location:
            query = re.sub(r'LOCATION.*["\']', '', in_sql)
        else:
            query = in_sql.replace('THELOC', self.location)
        return query


class SimpleFillSQL(SQLResolver):
    def __init__(self, *params: str):
        self.params = params

    def resolve(self, in_sql: str):
        return in_sql.format(*self.params)


class CreateTable(SparkAndLog):

    def __init__(self, name: str, schema: str, partition_cols: StructType = None, location: str = None):
        super().__init__()
        self.table_name = name
        self.loc = LocationSQL(location)
        self.part = PartitionSQL(partition_cols)
        self.fill = SimpleFillSQL(name, schema)

    def create(self):
        query = ResolverPipeline(stages=[self.loc, self.part, self.fill]).resolve(CREATE_TABLE)
        self.spark.sql(query)
        return self.spark.table(self.table_name)
