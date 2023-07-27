#!/usr/bin/env python3

__author__ = "Sachin duhan"

"""Job Factory to create Scheduler Jobs"""

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger


class JobFactory:
    """Factory class to generate jobs for APSchedulerConfig."""

    @staticmethod
    def create_job(func, trigger_type, trigger_args, job_id, args):
        """Create a new job."""
        if trigger_type == "interval":
            trigger = IntervalTrigger(**trigger_args)
        elif trigger_type == "date":
            trigger = DateTrigger(**trigger_args)
        elif trigger_type == "cron":
            trigger = CronTrigger(**trigger_args)
        else:
            raise ValueError("Invalid trigger type")

        return {
            "func": func,
            "id": job_id,
            "args": args,
            "trigger": trigger,
        }
