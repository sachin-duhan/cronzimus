#!/usr/bin/env python3

__author__ = "Sachin duhan"

"""Sample taks job template"""

import logging

from cronzimus.common.db import Database

LOGGER = logging.getLogger(__file__)


def task(db: Database):
    logging.info("Task executed successfully.")
    return isinstance(db, Database)
