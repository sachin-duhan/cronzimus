#!/usr/bin/env python3

__author__ = "Sachin duhan"

import logging

from cronzimus.common.logger import init_logger


def bootstrap_app():
    # TODO: load dynacof config.
    init_logger()

    logging.info("env setup completed")
