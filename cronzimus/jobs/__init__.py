#!/usr/bin/env python3

__author__ = "Sachin duhan"

"""Config file for Cronzimus scheduler"""

from typing import Dict, List

from cronzimus.common.db import Database
from cronzimus.controller.task import task
from cronzimus.jobs.job_factory import JobFactory

# import other adhoc taks files here.


class APSchedulerConfig:
    """Service scheduler for rules."""

    # ? INFO - https://github.com/viniciuschiele/flask-apscheduler/blob/master/examples/advanced.py

    def __init__(self, connection: Database) -> None:
        self.db = connection

    SCHEDULER_API_ENABLED = True

    @property
    def JOBS(self) -> List[Dict[str, any]]:
        jobs = []

        # Use the JobFactory to create jobs
        # Example usage for IntervalTrigger: {"trigger_type": "interval", "trigger_args": {"seconds": 5}}
        jobs.append(
            JobFactory.create_job(
                func=task,
                trigger_type="interval",
                trigger_args={"seconds": 5},
                job_id="sample_task",
                args=(self.db,),
            )
        )

        # Example usage for DateTrigger: {"trigger_type": "date", "trigger_args": {"run_date": some_datetime}}
        # Example usage for CronTrigger: {"trigger_type": "cron", "trigger_args": {"second": "0-59/10"}}
        # Add more jobs here if needed

        return jobs
