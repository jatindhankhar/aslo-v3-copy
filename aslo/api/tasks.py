from aslo.celery_app import celery, logger
from .release import handle_release
from .exceptions import ReleaseError, BuildProcessError


@celery.task(bind=True)
def release_process(self, gh_json):
    try:
        handle_release(gh_json)

    except (ReleaseError, BuildProcessError):
        logger.exception("Error in activity release process!")
    else:
        logger.info('Activity release process has finished successfully!')
