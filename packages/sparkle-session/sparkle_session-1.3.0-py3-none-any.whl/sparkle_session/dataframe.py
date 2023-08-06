from types import MethodType
from typing import Union, Tuple, Type

from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.functions import max as s_max, min as s_min
from pyspark.sql.types import DataType, StructType

from sparkle_session import SparkleStructType, sparkle_struct_type
from sparkle_session.create_table import CreateTable
from sparkle_session.session import SparkleSession, session_sparkle
from sparkle_session.utils import to_instance


def agg_sparkle(self, *exprs):
    r = self.agg_orig(*exprs)
    return sparkle_df(r)


# noinspection PyPep8Naming
class SparkleDataFrame(DataFrame):
    def any(self, condition) -> bool:
        return self.filter(condition).first() is not None

    def all(self, condition) -> bool:
        return self.filter(condition).count() == self.count()

    def easyUnion(self, df: 'SparkleDataFrame', trim_colums=False, expand_columns=False):
        if self.hasSameColumns(df):
            return self.union(df.select(*self.columns))
        else:
            raise NotImplementedError("Only supporting same columns for now")

    def isEmpty(self):
        return self.rdd.isEmpty()

    def hasSameColumns(self, other: DataFrame):
        my_cols = self.col_set
        them_cols = other.col_set
        return my_cols == them_cols

    def maxValue(self, col_name: str):
        return self.select(s_max(col_name).alias('max_val')).first().max_val

    def minValue(self, col_name: str):
        return self.select(s_min(col_name).alias('min_val')).first().min_val

    def cast(self, col_name: str, new_type: str):
        return self.withColumn(col_name, col(col_name).cast(new_type))

    @property
    def col_set(self):
        return set(self.columns)

    def requireColumn(self, *name: Union[str, Tuple[str, Type[DataType]]]):
        for n in name:
            if isinstance(n, str):
                assert n in self.columns, "Expecting column {} to exist in {}".format(n, self.columns)
            else:
                assert isinstance(n, Tuple), "Unexpected type {}".format(type(n))
                t = to_instance(n[1])
                name_type_found = any([f.name == n[0] and f.dataType == t for f in self.schema.fields])
                assert name_type_found, "Column '{}' of type {} not present in {}".format(n[0], n[1],
                                                                                          self.schema.fields)

    def createTable(self, table_name: str, partition_cols: StructType = None, location: str = None) -> DataFrame:
        """
        Create a table using this dataframe's schema

        :param table_name: name of table to be created
        :param partition_cols: partition columns to add
        :param location: path for external table
        :return: the table as dataframe
        """
        partition_fields = getattr(partition_cols, 'fieldNames', [])
        return CreateTable(table_name, self.toDDL(partition_fields),
                           partition_cols=partition_cols, location=location).create()

    @property
    def spark(self) -> SparkleSession:
        return session_sparkle(self.sql_ctx.sparkSession)

    def toDDL(self, *exclude: str):
        """
        Returns a string containing a schema in DDL format (e.g. `a` BIGINT, `b' STRING).
        """
        schema = self._jdf.schema()
        if exclude:
            schema = self._drop_fields(schema, *exclude)
        return schema.toDDL()

    def dropOfType(self, tipe, *exclude: str) -> 'SparkleDataFrame':
        s = self.schema.colsOfType(tipe, *exclude)
        return sparkle_df(self.drop(*s))

    @DataFrame.schema.getter
    def schema(self) -> SparkleStructType:
        return sparkle_struct_type(super().schema)

    def _drop_fields(self, j_schema, *to_drop: str):
        fields = [f for f in j_schema.fields() if f.name() not in to_drop]
        java_array = self._sc._gateway.new_array(self._sc._gateway.jvm.org.apache.spark.sql.types.StructField,
                                                 len(fields))
        for i in range(len(fields)):
            java_array[i] = fields[i]

        return self._sc._jvm.org.apache.spark.sql.types.StructType(java_array)

    def __getattribute__(self, name: str):
        attr = object.__getattribute__(self, name)
        if not name.startswith('_') and hasattr(attr, '__call__'):
            def sparkle_result(*args, **kwargs):
                result = attr(*args, **kwargs)
                if isinstance(result, DataFrame):
                    return sparkle_df(result)
                return result

            return sparkle_result
        else:
            return attr

    def groupBy(self, *cols):
        g = super().groupBy(*cols)
        g.agg_orig = g.agg
        g.agg = MethodType(agg_sparkle, g)
        return g


DataFrame.isEmpty = SparkleDataFrame.isEmpty
DataFrame.any = SparkleDataFrame.any
DataFrame.all = SparkleDataFrame.all
DataFrame.sparkle_union = SparkleDataFrame.easyUnion
DataFrame.hasSameColumns = SparkleDataFrame.hasSameColumns
DataFrame.requireColumn = SparkleDataFrame.requireColumn
DataFrame.maxValue = SparkleDataFrame.maxValue
DataFrame.minValue = SparkleDataFrame.minValue
DataFrame.cast = SparkleDataFrame.cast
DataFrame.toDDL = SparkleDataFrame.toDDL
DataFrame.dropOfType = SparkleDataFrame.dropOfType


# DataFrame.sparkle_schema = SparkleDataFrame.sparkle_schema

def extend_instance(obj, cls):
    """Apply mixins to a class instance after creation"""
    base_cls = obj.__class__
    base_cls_name = obj.__class__.__name__
    obj.__class__ = type(base_cls_name, (base_cls, cls), {})


def sparkle_df(df: DataFrame) -> SparkleDataFrame:
    df.__class__ = type('SparkleDataFrame', (SparkleDataFrame,), {})
    # noinspection PyTypeChecker
    return df
