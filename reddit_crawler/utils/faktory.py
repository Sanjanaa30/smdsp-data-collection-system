import datetime
import os
from typing import Callable, Optional

from dotenv import load_dotenv
from logger import logger
from pyfaktory import Client, Consumer, Job, Producer

load_dotenv()


def init_faktory_client(
    role: str,
    queue: str,
    jobtype: str,
    fn: Optional[Callable] = None,
    delayedTimer: Optional[datetime.timedelta] = None,
    args: Optional[list] = None,
):
    logger.debug("Role: %s queue: %s, jobtype: %s", role, queue, jobtype)
    faktory_server_url = os.getenv("FACTORY_SERVER_URL")
    logger.debug(f"Faktory server URL: {faktory_server_url}")
    try:
        if role == "consumer":
            with Client(faktory_url=faktory_server_url, role="consumer") as client:
                consumer = Consumer(
                    client=client,
                    queues=["default"] + [queue],
                    concurrency=2,
                )
                consumer.register(jobtype, fn)
                consumer.run()
        elif role == "producer":
            with Client(faktory_url=faktory_server_url, role="producer") as client:
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

    except Exception as e:
        logger.debug(f"Error connecting to Faktory server: {e}")
