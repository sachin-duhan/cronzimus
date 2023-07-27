from unittest import TestCase

from cronzimus.common.db import Database
from cronzimus.controller.task import task


class TestTask(TestCase):
    def test_task_execution(self):
        db = Database()
        self.assertTrue(task(db))

    def test_task_args(self):
        db = Database().connection
        self.assertFalse(task(db))
