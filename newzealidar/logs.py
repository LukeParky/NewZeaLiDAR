# -*- coding: utf-8 -*-
"""
This module contains logging functions for the package.
"""
import json
import logging
import logging.config
import os
import pathlib
import time
import warnings
from typing import Union

from newzealidar import utils


class FilterRecords(logging.Filter):
    def __init__(self, name="", module="", func="", msg=""):
        super().__init__(name)
        # The name of the logger used to log the event represented by this LogRecord
        self.name = name
        # The full string path of the source file where the logging call was made
        self.module = module
        # The name of the function or method from which the logging call was invoked
        self.func = func
        # The event description message
        self.msg = msg

    def filter(self, record):
        if len(self.name):
            return not (self.name == record.name)
        if len(self.module):
            return not (self.module in record.pathname)
        if len(self.func):
            return not (self.func == record.funcName)
        if len(self.msg):
            return not (self.msg in record.msg)
        return True


def setup_logging(
    default_path="logging.json",
    default_level=None,
    filter_warnings=True,
    env_key="LOG_CFG",
):
    """
    Setup logging configuration
    """
    if filter_warnings:
        warnings.filterwarnings("ignore")

    if default_level is not None:
        for name in logging.Logger.manager.loggerDict.keys():
            logging.getLogger(name).setLevel(logging.ERROR)

    value = utils.get_env_variable(env_key)
    path = default_path
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    elif default_level is not None:
        logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=logging.INFO)

    # add custom filters to the root logger
    logging.getLogger().addFilter(FilterRecords(module="dem"))

def setup_logging2(log_level=logging.INFO):
    # Define the logging format and date format
    logging_format = "%(asctime)s | %(levelname)-8s | %(name)-30s %(lineno)4d | %(funcName)-50s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    # Create and configure the root logger with the specified log level and formats
    logging.basicConfig(level=log_level, format=logging_format, datefmt=date_format)
    # Enable capturing Python warnings and redirect them to the logging system
    logging.captureWarnings(True)
    # Suppress (ignore) Python warnings from appearing in the console
    warnings.simplefilter("ignore")
    # List of loggers to prevent messages from reaching the root logger
    loggers_to_exclude = [
        "urllib3",
        "fiona",
        "botocore",
        "pyproj",
        "asyncio",
        "rasterio",
        # "scrapy",
        "distributed",
        "s3transfer",
        "charset_normalizer"
    ]
    # Iterate through the loggers to exclude
    for logger_name in loggers_to_exclude:
        # Get the logger instance for each name in the list
        logger = logging.getLogger(logger_name)
        # Disable log message propagation from these loggers to the root logger
        logger.propagate = False# Define the logging format and date format
    logging_format = "%(asctime)s | %(levelname)-8s | %(name)-30s %(lineno)4d | %(funcName)-50s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    # Create and configure the root logger with the specified log level and formats
    logging.basicConfig(level=log_level, format=logging_format, datefmt=date_format)
    # Enable capturing Python warnings and redirect them to the logging system
    logging.captureWarnings(True)
    # Suppress (ignore) Python warnings from appearing in the console
    warnings.simplefilter("ignore")
    # List of loggers to prevent messages from reaching the root logger
    loggers_to_exclude = [
        "urllib3",
        "fiona",
        "botocore",
        "pyproj",
        "asyncio",
        "rasterio",
        "scrapy",
        "distributed",
        "s3transfer",
        "charset_normalizer"
    ]
    # Iterate through the loggers to exclude
    for logger_name in loggers_to_exclude:
        # Get the logger instance for each name in the list
        logger = logging.getLogger(logger_name)
        # Disable log message propagation from these loggers to the root logger
        logger.propagate = False

def print_logger():
    loggers = [logging.getLogger()]  # get the root logger
    loggers = loggers + [
        logging.getLogger(name) for name in logging.root.manager.loggerDict
    ]
    for i, l in enumerate(loggers):
        print(f"{i} - logger: {l.name} - level: {l.level}, handlers: {l.handlers}")


def log_setup(
    module, log_dir: Union[str, pathlib.Path] = None, level=logging.DEBUG
) -> None:
    """
    Setup logging for the package.
    """
    now = time.strftime("%Y%m%d-%H%M%S")
    if log_dir is None:
        # module = pathlib.Path(__file__).stem
        log_file = pathlib.Path(__file__).parent.parent / "logs" / f"{module}-{now}.log"
    else:
        log_file = pathlib.Path(log_dir) / f"{module}-{now}.log"
    pathlib.Path(log_file.parent).mkdir(parents=True, exist_ok=True)
    logging.disable(logging.NOTSET)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)7s %(name)6s %(module)10s::%(funcName)12s> %(message)s",
        handlers=[logging.FileHandler(log_file, mode="w"), logging.StreamHandler()],
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8",
        force=True,
    )
    logging.captureWarnings(True)
    logging.getLogger("py.warnings").setLevel(logging.ERROR)
    logging.getLogger("fiona").propagate = False
    logging.getLogger("urllib3").propagate = False
    logging.getLogger("botocore").propagate = False
    logging.getLogger("rasterio").propagate = False
    logging.getLogger("boto3").propagate = False
    logging.getLogger("asyncio").propagate = False
    logging.getLogger("scrapy").propagate = False
    logging.getLogger("distributed").propagate = False
