#!/usr/bin/env python3

__author__ = "Sachin duhan"

"""Utility file to manage Env"""

import logging
import os

LOGGER = logging.getLogger(__file__)


class Env:
    DEV = "development"
    STAGING = "staging"
    PRODUCTION = "production"

    @property
    def current():
        return os.getenv("environment", os.getenv("env", Env.DEV))


if __name__ == "__test__":
    LOGGER.info(Env.current)
    LOGGER.info(f"dev mode - {Env.current == Env.DEV}")
