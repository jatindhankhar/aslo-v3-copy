from aslo.celery_app import celery, logger
from .release import handle_release
from .exceptions import ReleaseError, BuildProcessError
from .gh import find_tag_commit, comment_on_commit


@celery.task(bind=True)
def release_process(self, gh_json):
    try:
        handle_release(gh_json)
    except (ReleaseError, BuildProcessError) as error:
        logger.exception("Error in activity release process!")
        tag_commit = find_tag_commit(
            gh_json['repository']['full_name'], gh_json['release']['tag_name'])
        comment_on_commit(
            tag_commit, "Build Failed :x: Details:  {}".format(error))
    else:
        logger.info('Activity release process has finished successfully!')
        tag_commit = find_tag_commit(
            gh_json['repository']['full_name'], gh_json['release']['tag_name'])
        comment_on_commit(
            tag_commit, "Build Passed :white_check_mark:  Download url will be provided soon :link:")
