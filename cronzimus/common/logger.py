#!/usr/bin/env python3

__author__ = "Sachin duhan"

import logging
import sys

try:
    from loguru import logger

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

except Exception:
    pass


def init_logger(config: dict = {}):
    log_level: str = "INFO"
    log_fmt: str = "[%(levelname)s] - %(message)s"
    # TODO: {name}:{function}:{line} -> does not gives log file name debugging needed.
    loguru_format = "{time} - <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{level.icon} [{level}] - {message}</level>"
    date_fmt: str = "%Y-%m-%d %H:%M:%S"

    if config is not None:
        log_level = config.get("loglevel", "INFO")
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            numeric_level = getattr(logging, "INFO", None)
        log_fmt = config.get("logging_format", log_fmt)
        date_fmt = config.get("logging_datefmt", date_fmt)

    if "loguru" in sys.modules:
        loguru_format = config.get("loguru_format", loguru_format)
        loguru_config = {
            "handlers": [
                {"sink": sys.stdout, "format": loguru_format, "colorize": True},
                {
                    "sink": "server.log",
                    "serialize": True,
                    "enqueue": True,
                    "rotation": "512MB",
                },
            ]
        }
        logger.configure(**loguru_config)
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=numeric_level,
            format=log_fmt,
            datefmt=date_fmt,
            force=True,
        )
    else:
        # use standard logger
        logging.basicConfig(
            level=numeric_level,
            format=log_fmt,
            datefmt=date_fmt,
            force=True,
        )

    # "Register" new logging level to be compatible with loguru's success level
    SUCCESS = 35
    logging.addLevelName(SUCCESS, "SUCCESS")
    logging.Logger.success = success


def success(self, msg, *args, **kwargs):
    SUCCESS = 35
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, msg, args, **kwargs)
