import logging
from celery import Celery
from celery.utils.log import get_task_logger

celery = Celery(__name__)
TaskBase = celery.Task
logger = get_task_logger(__name__)


def init_celery(app):
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.config_from_object(app.config, namespace='CELERY')
    app.celery = celery

    # logging
    logger.setLevel(logging.INFO)
    if app.config['DEBUG']:
        logger.setLevel(logging.DEBUG)
