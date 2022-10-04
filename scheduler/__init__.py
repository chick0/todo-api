from os import environ
from logging import getLogger
from datetime import datetime
from datetime import timedelta

from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from .db import factory
from app.models import History
from app.models import DBSession

if "SCHEDULER_TIMEZONE" not in environ:
    load_dotenv()

logger = getLogger()
scheduler = BlockingScheduler(timezone=environ['SCHEDULER_TIMEZONE'])


@scheduler.scheduled_job("cron", hour="3")
def delete_expired_session():
    logger.info("Try to delete expired DBSession")
    session = factory()

    result = session.query(DBSession).filter(
        DBSession.dropped_at < datetime.now()
    ).delete()

    session.commit()

    logger.info(f"{result} sessions have been deleted.")
    session.close()


@scheduler.scheduled_job("cron", hour="4")
def delete_login_history():
    logger.info("Try to delete login history")
    session = factory()

    date = datetime.now() - timedelta(days=31 * 3)

    result = session.query(History).filter(
        History.created_at < date
    ).delete()

    session.commit()

    logger.info(f"{result} login histories have been deleted.")
    session.close()
