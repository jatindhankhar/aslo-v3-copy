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
        build.invoke_build(name)

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
        build.invoke_asset_build(bundle_name)
        
        if bundle_name:
           activity_file = utils.check_bundle(bundle_name)
           if activity_file:
               activity_file = activity_file.decode()
               parser = utils.read_activity(activity_file,is_string=True)
               print("Manifest Parsed .. OK")
               # Check versions before invoking build
               json_object = utils.get_activity_manifest(parser)
               print("JSON Parsed .. OK")
               print(json_object)
               if is_a_new_release(json_object) is False:
                     # TODO - Inform Author about Failure
                    return "Failure"
               print("Version check .. OK")
               update_activity_record(json_object)

    except BuildProcessError as e:
        logger.exception("Error in activity building process")
        return False