import datetime
import os
from typing import Callable, Optional
from pathlib import Path
from dotenv import load_dotenv
from utils.logger import Logger
from pyfaktory import Client, Consumer, Job, Producer
from constants.constants import (
    CHAN_CRAWLER,
    FAKTORY_SERVER_URL,
    FAKTORY_CONSUMER_ROLE,
    FAKTORY_PRODUCER_ROLE,
)

# Load environment from the package .env to ensure consistent behavior
# regardless of current working directory (aligns with plsql.py)
# Load only the package-specific .env to avoid picking up unrelated root env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logger = Logger(CHAN_CRAWLER).get_logger()


def initialize_consumer(
    queue: list, jobtypes: list, fn: Optional[Callable] = None, concurrency: int = 2
):
    logger.info("Initialing Consumer")
    logger.debug("queue: %s, jobtype: %s", queue, jobtypes)
    faktory_server_url = os.getenv(FAKTORY_SERVER_URL)
    logger.debug(f"Faktory server URL: {faktory_server_url}")

    try:
        with Client(
            faktory_url=faktory_server_url, role=FAKTORY_CONSUMER_ROLE
        ) as client:
            consumer = Consumer(
                client=client,
                queues=["default"] + queue,
                concurrency=concurrency,
            )
            for jobtype in jobtypes:
                consumer.register(jobtype, fn)
            consumer.run()

    except Exception as e:
        logger.debug(f"Error connecting to Faktory server: {e}")


def initialize_producer(
    queue: str,
    jobtype: str,
    delayedTimer: Optional[datetime.timedelta] = None,
    args: Optional[list] = None,
):
    logger.info("Initialing Producer")
    logger.debug("queue: %s, jobtype: %s", queue, jobtype)
    faktory_server_url = os.getenv(FAKTORY_SERVER_URL)
    logger.debug(f"Faktory server URL: {faktory_server_url}")
    with Client(faktory_url=faktory_server_url, role=FAKTORY_PRODUCER_ROLE) as client:

            # NEW: default to zero delay if None
        if delayedTimer is None:
            delayedTimer = datetime.timedelta(seconds=0)

        run_at = datetime.datetime.now(datetime.UTC) + delayedTimer
        run_at = run_at.isoformat()[:-7] + "Z"
        # logger.info(f"run_at = {run_at}")
        producer = Producer(client=client)
        job = Job(
            jobtype=jobtype,
            queue=queue,
            args=args or [],
            at=str(run_at),
        )
        producer.push(job)
    logger.info(
        "Scheduled job '%s' on queue '%s' to run at %s",
        jobtype,
        queue,
        run_at,
    )
