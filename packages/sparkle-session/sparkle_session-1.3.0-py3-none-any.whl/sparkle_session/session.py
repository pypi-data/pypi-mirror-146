import collections
import inspect

import re
import types
from collections.abc import Iterable

from pyspark import _NoValue
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.conf import RuntimeConfig
from pyspark.sql.types import StructType

from sparkle_session.spark_logger import Logger
from sparkle_session.utils import get_class_name

# noinspection PyPep8Naming
APP_ENV = "spark.app.env"
ENV_NAME = "spark.app.{}.env_name"


class SparkleConf(RuntimeConfig):

    # noinspection PyPep8Naming
    def conf_get(self, key: str, defaultValue=_NoValue):
        if self._app_env() and "spark.app" in key:
            val = self._get_from_env(key)
            return self._replace_in_val(val)
        else:
            return self.orig_get(key, defaultValue)

    def _get_from_env(self, key):
        env_sub = r'spark.app.{}.\1'.format(self.currentEnv())
        env_key = re.sub(r'spark\.app.(.*)', env_sub, key)
        val = self.orig_get(env_key, self.orig_get(key, None))
        return val

    # noinspection PyPep8Naming
    def currentEnv(self) -> str:
        return self.orig_get(APP_ENV)

    # noinspection PyPep8Naming
    def get_bool(self, key, defaultValue=_NoValue):
        return str(self.get(key, defaultValue)).lower() in ['true', 'yes']

    def orig_get(self, key: str, defaultValue=_NoValue) -> str:
        pass

    def _app_env(self):
        return self.orig_get(APP_ENV, "")

    def _short_env_name(self):
        if self._get_from_env('spark.app.short_name') is not None:
            return self._get_from_env('spark.app.short_name')
        else:
            return self._app_env()

    def _full_env_name(self):
        if self._get_from_env('spark.app.full_name') is not None:
            return self._get_from_env('spark.app.full_name')
        else:
            return {'acc': 'acceptance', 'dev': 'development', 'prod': 'production'}[self._app_env()]

    def _replace_in_val(self, v: str):
        if v:
            v = re.sub(r'\s*{{\s*env\s*}}\s*', self._short_env_name(), v)
            v = re.sub(r'\s*{{\s*env_name\s*}}\s*', self._full_env_name(), v)
            v = v.replace('//', '/')
            if v.startswith("_"):
                v = v.replace("_", "", 1)
        return v


class SparkleSession(SparkSession):
    def __init__(self, sparkContext):
        self._jvm = ...
        super().__init__(sparkContext)

    # noinspection PyPep8Naming
    def emptyDataFrame(self) -> DataFrame:
        schema = StructType([])
        return self.createDataFrame(self.sparkContext.emptyRDD(), schema)

    def log(self, name: str = None, log_level: str = None) -> Logger:
        if not name:
            name = get_class_name(inspect.stack()[1][0])
        log4j_ = self._jvm.org.apache.log4j
        logger = log4j_.LogManager.getLogger(name)
        if log_level:
            logger.setLevel(log4j_.Level.toLevel(log_level))
            logger.info("logger set to {}".format(log_level))

        def dbg(lgr, msg: str, format_args):
            # noinspection PyUnresolvedReferences
            """
                Laizy evaluation of debug code

                >>> log.dbg("Count of my df: {}", lambda: df.cache().count())
                :param lgr:
                :param msg: The log string with optional {}s in it
                :param format_args: a function that when called returns a list of the arguments for str.format()
                :return:
            """

            if lgr.isDebugEnabled():
                args = format_args()
                if isinstance(args, Iterable):
                    lgr.debug(msg.format(*args))
                else:
                    lgr.debug(msg.format(args))

        logger.dbg = types.MethodType(dbg, logger)

        return logger

    @property
    def conf(self) -> 'SparkleConf':
        c = super().conf

        def _is_original_get():
            return c.get.__qualname__ == RuntimeConfig.get.__qualname__

        if not isinstance(c, SparkleConf) or _is_original_get():
            c.currentEnv = types.MethodType(SparkleConf.currentEnv, c)
            c.orig_get = c.get
            c.get = types.MethodType(SparkleConf.conf_get, c)
            c.get_bool = types.MethodType(SparkleConf.get_bool, c)
            c.__class__ = SparkleConf
        return c


def session_sparkle(spark) -> SparkleSession:
    spark.__class__ = SparkleSession
    return spark


def sparkle_session(spark) -> SparkSession:
    return session_sparkle(spark)


def current_sparkle_session():
    return session_sparkle(SparkSession.builder.getOrCreate())
