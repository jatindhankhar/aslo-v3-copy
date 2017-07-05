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
        # Insert/Override repository tag
        activity['repository'] = url
        repo_location = build.get_repo_location(name)
        build.invoke_build(name)
        translations = build.get_translations(repo_location)
        processed_images = build.process_image_assets(activity, repo_location)
        activity['platform_versions'] = build.get_platform_versions(
            activity, repo_location)
        activity['release_info'] = {}
        activity['release_info']['release_notes'] = gh_json['release']['body']
        activity['release_info']['release_time'] = gh_json['release']['published_at']
        build.clean_repo(name)
        build.populate_database(activity, translations, processed_images)
        logger.info(activity)
        logger.info(processed_images)
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
        # Insert/Override repository tag
        activity['repository'] = url
        extracted_bundle = build.extract_bundle(bundle_name)
        processed_images = build.process_image_assets(
            activity, extracted_bundle)
        activity['platform_versions'] = build.get_platform_versions(
            activity, extracted_bundle)
        activity['release_info'] = {}
        activity['release_info']['release_notes'] = gh_json['release']['body']
        activity['release_info']['release_time'] = gh_json['release']['published_at']

        translations = build.get_xo_translations(extracted_bundle)
        build.populate_database(activity, translations, processed_images)
        logger.info(processed_images)
        logger.info(translations["es"])
        logger.info(activity)

    except BuildProcessError as e:
        logger.exception("Error in activity building process")
        return False
