import logging
from pathlib import Path
from typing import Any, TextIO

from colorama import Fore

import beni
import beni.print as bprint

_loggerName = 'beni'

_countWarning: int = 0
_countError: int = 0
_countCritical: int = 0


def init(loggerName: str = '', loggerLevel: int = logging.INFO, logFile: Path | None = None):
    LOGGER_FORMAT = '%(asctime)s %(levelname)-1s %(message)s', '%Y-%m-%d %H:%M:%S'
    LOGGER_LEVEL_NAME = {
        logging.DEBUG: 'D',
        logging.INFO: '',
        logging.WARNING: 'W',
        logging.ERROR: 'E',
        logging.CRITICAL: 'C',
    }

    if loggerName:
        global _loggerName
        _loggerName = loggerName

    logger = logging.getLogger(_loggerName)
    logger.setLevel(loggerLevel)
    for loggingLevel, value in LOGGER_LEVEL_NAME.items():
        logging.addLevelName(loggingLevel, value)

    loggerFormatter = logging.Formatter(*LOGGER_FORMAT)

    class CustomStreamHandler(logging.StreamHandler):

        stream: TextIO

        def emit(self, record: logging.LogRecord):
            try:
                msg = self.format(record) + self.terminator
                # issue 35046: merged two stream.writes into one.
                func = self.stream.write
                if record.levelno == logging.WARNING:
                    global _countWarning
                    _countWarning += 1
                    bprint.set_color(Fore.LIGHTYELLOW_EX)

                elif record.levelno == logging.ERROR:
                    global _countError
                    _countError += 1
                    bprint.set_color(Fore.LIGHTRED_EX)
                elif record.levelno == logging.CRITICAL:
                    global _countCritical
                    _countCritical += 1
                    bprint.set_color(Fore.LIGHTMAGENTA_EX)
                func(msg)
                bprint.clear_color()
                self.flush()
            except RecursionError:  # See issue 36272
                raise
            except Exception:
                self.handleError(record)

    loggerHandler = CustomStreamHandler()
    loggerHandler.setFormatter(loggerFormatter)
    loggerHandler.setLevel(loggerLevel)
    logger.addHandler(loggerHandler)

    if logFile:
        beni.makedir(logFile.parent)
        fileLoggerHandler = logging.FileHandler(logFile, delay=True)
        fileLoggerHandler.setFormatter(loggerFormatter)
        fileLoggerHandler.setLevel(loggerLevel)
        logger.addHandler(fileLoggerHandler)


def debug(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).debug(msg, *args, **kwargs)


def info(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).info(msg, *args, **kwargs)


def warning(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).warning(msg, *args, **kwargs)


def error(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).error(msg, *args, **kwargs)


def critical(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).critical(msg, *args, **kwargs)


def getcount_warning():
    return _countWarning


def setcount_warning(value: int):
    global _countWarning
    _countWarning = value


def getcount_error():
    return _countError


def setcount_error(value: int):
    global _countError
    _countError = value


def getcount_critical():
    return _countCritical


def setcount_critical(value: int):
    global _countCritical
    _countCritical = value
