from abc import ABC
from typing import Callable, List


class Logger(ABC):

    def debug(self, msg: str):
        pass

    def info(self, msg: str):
        pass

    def warn(self, msg: str):
        pass

    def error(self, msg: str):
        pass

    def fatal(self, msg: str):
        pass

    # noinspection PyPep8Naming
    def isDebugEnabled(self) -> bool:
        pass

    # noinspection PyPep8Naming
    def isInfoEnabled(self) -> bool:
        pass

    def dbg(self, msg: str, f: Callable[[], List]):
        """
        Lazy evaluating logging. Only if debug level is enabled, the f will be called

        Example: log.dbg("df1 count: {}, df2 count: {}", lambda: (df1.count(), df2.count()) )
        :param msg: message with {} for formatting
        :param f: function that produces the arguments to str.format()
        """""
        pass
