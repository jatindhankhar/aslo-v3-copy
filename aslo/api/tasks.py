from . import build
from aslo.celery_app import celery, logger
from .exceptions import BuildProcessError


@celery.task(bind=True)
def build_process(self, gh_json):
    try:
        url = gh_json['repository']['clone_url']
        name = gh_json['repository']['name']
        tag = gh_json['release']['tag_name']

        # TODO: work on cases (bundle attached or not)
        # and insert data into DB

        build.clone_repo(url, name, tag)
        activity = build.get_activity_metadata(name)
        build.invoke_build(name)

    except BuildProcessError as e:
        logger.exception("Error in activity building process")
        return False

    logger.info('Activity building process finished succesfully!')
