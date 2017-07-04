from . import build
from aslo.celery_app import celery, logger
from .exceptions import BuildProcessError


@celery.task(bind=True)
def build_process(self, gh_json):
    try:
        release = gh_json['release']
        # TODO: work on cases (bundle attached or not)
        # and insert data into DB
        # Invoke different build programs depending upon whether it's a source/asset release
        if 'assets' in release and len(release['assets']) != 0:
            handle_asset_release(gh_json)
        else:
            handle_source_release(gh_json)

    except BuildProcessError as e:
        logger.exception("Error in activity building process")
        return False

    logger.info('Activity building process finished !')


def handle_source_release(gh_json):
    logger.info('Building for a source release')
    try:
        url = gh_json['repository']['clone_url']
        name = gh_json['repository']['name']
        release = gh_json['release']
        tag = release['tag_name']

        build.clone_repo(url, name, tag)
        activity = build.get_activity_metadata(name)
        
        # TODO: Couple out clean repo so we can avoid uploading screenshots for yet to fail builds
        # Upload icons 
        # Get translations string invoking build, since we clean the repo afterwards
        translations = build.get_translations(build.get_repo_location(name))
        imgur_links = build.upload_image_assets(activity,build.get_repo_location(name))  
        build.invoke_build(name)
        logger.info(activity)
        logger.info(translations["es"])
    except BuildProcessError as e:
        logger.exception("Error in activity building process")
        return False


def handle_asset_release(gh_json):
    logger.info('Building for a asset release')
    try:
        url = gh_json['repository']['clone_url']
        name = gh_json['repository']['name']
        release = gh_json['release']
        tag = release['tag_name']

        bundle_name = build.check_and_download_assets(release['assets'])
        activity = build.invoke_asset_build(bundle_name)
        translations = build.get_xo_translations(bundle_name)
        logger.info(translations["es"])
        logger.info(activity)

    except BuildProcessError as e:
        logger.exception("Error in activity building process")
        return False
