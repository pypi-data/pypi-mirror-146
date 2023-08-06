import inspect
from typing import Union, List

from pyspark.sql.types import StructType, DataType, StructField


def _field_is(field: StructField, tipe: Union[str, Union[DataType, type]]) -> bool:
    if isinstance(tipe, str):
        return tipe.lower() == field.dataType.typeName() or tipe.lower() == field.dataType.simpleString()
    else:
        if inspect.isclass(tipe):
            return isinstance(field.dataType, tipe)
        else:
            return field.dataType.simpleString() == tipe.simpleString()


class SparkleStructType(StructType):

    # noinspection PyPep8Naming
    def colsOfType(self, tipe: Union[str, Union[DataType, type]], *exclude: str) -> List[str]:
        return [f.name for f in self.ofType(tipe, *exclude)]

    # noinspection PyPep8Naming
    def ofType(self, tipe: Union[str, DataType], *exclude: str) -> List[StructField]:
        return [f for f in self.fields if _field_is(f, tipe) and f.name not in exclude]


def sparkle_struct_type(s):
    s.__class__ = SparkleStructType
    return s


StructType.colsOfType = SparkleStructType.colsOfType
StructType.ofType = SparkleStructType.ofType
