#!/usr/bin/env python3

__author__ = "Sachin duhan"

import logging

from flask import Flask, jsonify
from flask_apscheduler import APScheduler

from cronzimus.common.db import Database
from cronzimus.config import bootstrap_app
from cronzimus.jobs import APSchedulerConfig

LOGGER = logging.getLogger(__file__)

app = Flask(__name__)
scheduler = APScheduler()


@app.get("/api/health")
def health():
    return jsonify({"status": "running"}, status=200)


# TODO: use dynaconf
def main():
    bootstrap_app()

    # global db connection
    db_connection = Database()

    app.config.from_object(APSchedulerConfig(db_connection))
    scheduler.init_app(app=app)

    scheduler.start()
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
