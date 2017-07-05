import os
import shutil
import configparser
import base64
import datetime
from flask import current_app as app
from aslo.celery_app import logger
from subprocess import call
from polib import pofile
from .exceptions import BuildProcessError
import requests
import zipfile
import json
from glob import glob
import uuid
from mongoengine import connect
from aslo.models.Activity import MetaData, Release, Developer, Summary, Name
from imgurpython import ImgurClient


def get_translations(activity_location):
    po_files_location = os.path.join(activity_location, 'po/')
    translations = {}

    def get_language_code(filepath):
        basename = os.path.basename(filepath)
        return os.path.splitext(basename)[0]

    matched_files = glob(os.path.join(po_files_location, "*.po"))
    if len(matched_files) == 0:
        raise BuildProcessError(
            "No po files found at location . %s", po_files_location)

    po_files = list(map(pofile, matched_files))
    language_codes = list(map(get_language_code, matched_files))

    # Intialize the dictionary
    for language_code in language_codes:
        translations[language_code] = {}

    for po_file, language_code in zip(po_files, language_codes):
        for entry in po_file.translated_entries():
            # print(entry)
            translations[language_code][entry.msgid] = entry.msgstr

    return translations


def process_image_assets(attribute_dict, activity_location):
    """Processes all image assets and uploads screenshots to Imgur.

    Args:
        attribute_dict: Dictionary containing activity.info attributes
        repo_location: Location where repo/bundle is stored
    Returns:
        A dict having icon and screesnhots keys containing imgur urls
    Raises:
        BuildProcessErorr: When icon can't be uploaded due to netowrk issues or file being not present
    """
    imgur_client = ImgurClient(
        app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_SECRET'])
    processed_images = {"icon": "", "screenshots": []}
    if "icon" not in attribute_dict:
        raise BuildProcessError("Cannot find icons.")
    icon_path = os.path.join(
        activity_location, "activity", attribute_dict["icon"] + ".svg")
    processed_images["icon"] = convert_activity_icon(icon_path)

    if "screenshots" in attribute_dict:
        screenshot_links = upload_screenshots(
            attribute_dict["screenshots"].split(" "), urls=True)
        processed_images["screenshots"].extend(screenshot_links)

    screenshot_path = os.path.join(activity_location, "screenshots")
    if os.path.exists(screenshot_path):
        screenshots = glob(os.path.join(screenshot_path, "*.*"))
        processed_images["screenshots"].extend(upload_screenshots(screenshots))

    return processed_images


def convert_activity_icon(icon_path):
    """Convert activity icon to base64 encoded strign.

    Args:
        icon_path: Path where icon is stored
    Returns:
        Base64 encoded version of SVG Icon
    Raises:
        BuildProcessErorr: When icon can't be converted or not found
    """
    imgur_client = ImgurClient(
        app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_SECRET'])
    if not (os.path.exists(icon_path) and os.path.isfile(icon_path)):
        raise BuildProcessError("Cannot find icon at path %s", icon_path)

    try:
        logger.info("Icon path is %s", icon_path)
        with open(icon_path, "rb") as f:
            img_data = f.read()
        encoded_string = base64.b64encode(img_data).decode()
        return encoded_string
    except Exception as e:
        raise BuildProcessError(
            "Something unexpected happened while converting the icon. Exception Message %s", e)


def get_icon_path(icon_name, activity_name):
    """ Returns icon path for an activity.

    Args:
        icon_name: Name of the icon 
        activity_name: Name of the activity
    Returns:
       Icon path of the activity 
    Raises:
       None 
    """
    return os.path.join(get_repo_location(activity_name), "activity", icon_name + ".svg")


def get_repo_location(name):
    return os.path.join(app.config['BUILD_CLONE_REPO'], name)


def get_bundle_path(bundle_name):
    return os.path.join(app.config['BUILD_BUNDLE_DIR'], bundle_name)


def get_parser(activity_file, read_string=False):
    parser = configparser.ConfigParser()
    if read_string:
        try:
            parser.read_string(activity_file)
        except Exception as e:
            raise BuildProcessError(
                'Error parsing metadata file. Error : %s', e)
        else:
            return parser
    else:
        if len(parser.read(activity_file)) == 0:
            raise BuildProcessError('Error parsing metadata file')
        else:
            return parser


def validate_metadata_attributes(parser, attributes):
    MANDATORY_ATTRIBUTES = ['name', 'bundle_id', 'summary', 'license',
                            'categories', 'icon', 'activity_version', 'repository', 'activity_version']
    return all(parser.has_option('Activity', attribute) for attribute in attributes)


def upload_screenshots(screenshots, urls=False):
    """ Uploads screenshots to Imgur.

    Args:
        screenshots: List containing screenshots path or urls
        urls: Default  - False. Determines whether screenshots are paths or urls
    Returns:
        Returns a list containing coressponding imgur links
    Raises:
       None 
    """
    imgur_client = ImgurClient(
        app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_SECRET'])
    imgur_links = []
    if urls:
        for screenshot in screenshots:
            result = imgur_client.upload_from_url(screenshot)
            imgur_links.append(result['link'])
    else:
        for screenshot in screenshots:
            result = imgur_client.upload_from_path(screenshot)
            imgur_links.append(result['link'])
    return imgur_links


def check_and_download_assets(assets):

    def check_asset(asset):
        if asset_name_check(asset['name']):
            return asset_manifest_check(asset['browser_download_url'], asset['name'])
        return False

    def download_asset(download_url, name):
        response = requests.get(download_url, stream=True)
        # Save with every block of 1024 bytes
        logger.info("Downloading File .. " + name)
        with open(os.path.join(app.config['TEMP_BUNDLE_DIR'], name), "wb") as handle:
            for block in response.iter_content(chunk_size=1024):
                handle.write(block)
        return

    def check_info_file(name):
        logger.info("Checking For Activity.info")
        xo_file = zipfile.ZipFile(os.path.join(
            app.config['TEMP_BUNDLE_DIR'], name))
        return any("activity.info" in filename for filename in xo_file.namelist())

    def asset_name_check(asset_name):
        print("Checking for presence of .xo in name of " + asset_name)
        return ".xo" in asset_name

    def verify_bundle(bundle_name):
        bundle_path = get_bundle_path(bundle_name)
        return os.path.exists(bundle_path) and os.path.isfile(bundle_path)

    def asset_manifest_check(download_url, bundle_name):
        download_asset(download_url, bundle_name)
        if check_info_file(bundle_name):
            # Check if that bundle already exists then we don't continue
            # Return false if that particular bundle already exists
            if verify_bundle(bundle_name):
                os.remove(os.path.join(
                    app.config['TEMP_BUNDLE_DIR'], bundle_name))
                raise BuildProcessError('File %s already exits' % bundle_name)
            else:
                shutil.move(os.path.join(app.config['TEMP_BUNDLE_DIR'],
                                         bundle_name), app.config['BUILD_BUNDLE_DIR'])
                return bundle_name
        return False

    for asset in assets:
        bundle_name = check_asset(asset)
        if bundle_name:
            return bundle_name
    raise BuildProcessError(
        'No valid bundles were found in this asset release')


def clone_repo(url, name, tag):
    target_dir = app.config['BUILD_CLONE_REPO']
    if not os.path.isdir(target_dir):
        raise BuildProcessError('Directory %s does not exist' % target_dir)

    if os.path.isdir(get_repo_location(name)):
        logger.info('Removing existing cloned repo for %s', name)
        shutil.rmtree(get_repo_location(name))

    cmd = ['git', '-c', 'advice.detachedHead=false', '-C', target_dir,
           'clone', '-b', tag, '--depth', '1', url]

    logger.info('Cloning repo %s', url)
    if call(cmd) != 0:
        raise BuildProcessError('[%s] command has failed' % ' '.join(cmd))


def get_platform_versions(activity, repo_location):
    logger.info("Applying heurisitc to determine platform versions")

    def is_web():
        if 'exec' in activity:
            return activity['exec'] == 'sugar-activity-web'
        return False  # Fallback

    GTK3_IMPORT_TYPES = {'sugar3': 3, 'from gi.repository import Gtk': 3,
                         'sugar.': 2, 'import pygtk': 2, 'pygtk.require': 2}

    def is_gtk3():
        setup_py_path = os.path.join(repo_location, 'setup.py')
        all_files = os.listdir(repo_location)
        try_paths = [setup_py_path] + all_files

        for path in try_paths:
            if os.path.isfile(path):
                with open(path) as f:
                    text = f.read()
                    for sign in GTK3_IMPORT_TYPES:
                        if sign in text:
                            version = GTK3_IMPORT_TYPES[sign]
                            return version == 3

        # Fallback to assuming GTK3
        return True

    OLD_TOOLBAR_SIGNS = ['activity.ActivityToolbox', 'gtk.Toolbar']

    def has_old_toolbars():
        for path in os.listdir(repo_location):
            if os.path.isfile(path):
                with open(path) as f:
                    text = f.read()
                for sign in OLD_TOOLBAR_SIGNS:
                    if sign in text:
                        return True
        return False

    def determine_min_sugar_version(is_gtk3, is_web, has_old_toolbars):
        min_sugar_version = '0.100' if is_web else (
            '0.96' if is_gtk3 else (
                '0.86' if not has_old_toolbars else '0.82'
            ))
        return min_sugar_version

    platform_versions = {}
    platform_versions['is_gtk3'] = is_gtk3()
    platform_versions['is_web'] = is_web()
    platform_versions['has_old_toolbars'] = has_old_toolbars()
    platform_versions['min_sugar_version'] = determine_min_sugar_version(
        platform_versions['is_gtk3'], platform_versions['is_web'], platform_versions['has_old_toolbars'])

    return platform_versions


def get_activity_metadata(name):
    def metadata_file_exists():
        repo_dir = get_repo_location(name)
        activity_file = os.path.join(repo_dir, "activity/activity.info")
        if not os.path.isfile(activity_file):
            raise BuildProcessError(
                'Activity file %s does not exist', activity_file
            )

        return activity_file

    def parse_metadata_file():
        parser = get_parser(activity_file)
        try:
            attributes = dict(parser.items('Activity'))
        except configparser.NoSectionError as e:
            raise BuildProcessError(
                'Error parsing metadata file. Exception message: %s', e
            )

        return attributes

    activity_file = metadata_file_exists()
    return parse_metadata_file()


def clean_repo(repo_name):
    """ Deletes cloned repository.

    Args:
        repo_name: Name of the repository
    Returns:
        None
    Raises:
       None 
    """
    shutil.rmtree(get_repo_location(repo_name))


def invoke_build(name):
    def store_bundle():
        dist_dir = os.path.join(get_repo_location(name), 'dist')
        if os.path.isdir(dist_dir) and len(os.listdir(dist_dir)) == 1:
            bundle_name = os.path.join(dist_dir, os.listdir(dist_dir)[0])
        else:
            raise BuildProcessError('Bundle file was not generated correctly')

        try:
            shutil.copy2(bundle_name, app.config['BUILD_BUNDLE_DIR'])
            stored_bundle = os.path.join(
                app.config['BUILD_BUNDLE_DIR'],
                os.path.basename(bundle_name)
            )
            os.chmod(stored_bundle, 0o644)
        except IOError as e:
            raise BuildProcessError(
                'Bundle copying has failed: %s', e
            )

        logger.info('Bundle succesfully stored at %s', stored_bundle)

    volume = get_repo_location(name) + ':/activity'
    docker_image = app.config['BUILD_DOCKER_IMAGE']
    docker_cmd = ['docker', 'run', '--rm', '-v', volume, docker_image]
    logger.info('Running docker command: "%s"', ' '.join(docker_cmd))
    if call(docker_cmd) != 0:
        raise BuildProcessError('Docker building process has failed')

    store_bundle()


def populate_database(activity, translations, processed_images):
    """ Populates MongoDB with MONGO_DBNAME as the target table/collection

    Args:
        repo_name: Dictionary containing activity.info attributes
        translations: Dictionary containing translations
        processed_images: Dictionary processed icon and screenshots
    Returns:
        None
    Raises:
       BuildProccessError: When version numbers are not correct (less than the existing one in Database) or when Data cannot be inserted 
    """

    def translate_field(field_value, model_class):
        """ Helper function which translates a field value and prepares an object with language code as keys  

        Args:
            field_value: Value of the String to be converted
            model_class: Model class whose object needs to prepared for insertion
        Returns:
            Model class object populated with proper translations of the word if any 
        Raises:
            None
        """
        results = []
        for language_code in translations:
            if field_value in translations[language_code]:
                obj = model_class()
                obj[language_code] = field_value
                results.append(obj)
        return results

    connect(app.config['MONGO_DBNAME'])
    try:
        metadata = MetaData()
        metadata.name.extend(translate_field(activity['name'], Name))
        metadata.bundle_id = activity['bundle_id']
        if 'summary' in activity:
            summaries = translate_field(activity['summary'], Summary)
            metadata.summary.extend(summaries)
        if 'categories' in activity:
            metadata.categories = activity['categories']
        metadata.repository = activity['repository']
        metadata.icon = processed_images['icon']

        release = Release()
        release.activity_version = float(activity['activity_version'])
        release.release_notes = activity['release_info']['release_notes']
        release.download_url = "https://mock.org/download_url"
        release.min_sugar_version = float(
            activity['platform_versions']['min_sugar_version'])
        release.is_web = activity['platform_versions']['is_web']
        release.has_old_toolbars = activity['platform_versions']['has_old_toolbars']
        release.screenshots.extend(processed_images['screenshots'])
        release_time = datetime.datetime.strptime(
            activity['release_info']['release_time'], "%Y-%m-%dT%H:%M:%SZ")
        release.timestamp = release_time

        release.save()
        metadata.add_release(release)
        metadata.save()

    except Exception as e:
        metadata.delete()
        release.delete()
        raise BuildProcessError(
            "Failed to insert data inside the DB. Error : %s", e)


def clean_up(extact_dir):
    """ Delete extraction directory of bunlde
   Args:
       extract: Extraction path of bundle
   Returns:
       None
   Raises:
       None
   """
    shutil.rmtree(extact_dir)


def extract_bundle(bundle_name):
    """ Extracts bundle to random directory
    Args:
        bundle_name: Name of the bundle that needs to be extracted
    Returns:
        Path where bundle is extracted
    Raises:
        BuildProcessErorr: If file is corrupted and/or bundle cannot be extracted properly
    """
    logger.info("Extracting %s ....", bundle_name)
    try:
        xo_archive = zipfile.ZipFile(get_bundle_path(bundle_name))
        # Create a random UUID to store the extracted material
        random_uuid = uuid.uuid4().hex
        # Create the folder with name as random UUID
        extract_dir = os.path.join(app.config['TEMP_BUNDLE_DIR'], random_uuid)
        os.mkdir(extract_dir)
        archive_root_prefix = os.path.commonpath(xo_archive.namelist())
        xo_archive.extractall(path=extract_dir)
        extraction_path = os.path.join(extract_dir, archive_root_prefix)
        return extraction_path
    except Exception as e:
        if e.__class__.__name__ is "FileExistsError":
            clean_up(extract_dir)
        raise BuildProcessError(
            "Unable to open archive : %s. Error : %s ", bundle_name, e.__class__)


def get_xo_translations(extract_dir):
    """ Wrapper function  to crawl translations for a bundle
    Args:
        bundle_name: Directory where bunlde is extracted
    Returns:
        Dictionary containing translations
    Raises:
        None
    """
    return get_translations(extract_dir)


def invoke_asset_build(bundle_name):
    def remove_bundle(bundle_name):
        logger.info("Removing Bundle : %s", bundle_name)
        os.remove(get_bundle_path(bundle_name))

    def parse_metadata_file():
        parser = get_parser(activity_file, read_string=True)
        try:
            attributes = dict(parser.items('Activity'))
        except configparser.NoSectionError as e:
            raise BuildProcessError(
                'Error parsing metadata file. Exception message: %s', e
            )

        return attributes

    def check_bundle(bundle_name):
        xo_file = zipfile.ZipFile(get_bundle_path(bundle_name))
        # Find the acitivity_file and return it
        for filename in xo_file.namelist():
            if 'activity.info' in filename:
                return xo_file.read(filename)
        logger.info(
            'Bundle Check has failed. %s is not a valid bundle file ', bundle_name)
        raise BuildProcessError(
            'Bundle Check has failed. %s is not a valid bundle file ', bundle_name)

    try:
        activity_file = check_bundle(bundle_name)
        activity_file = activity_file.decode()
        return parse_metadata_file()
    except Exception as e:
        remove_bundle(bundle_name)
        raise BuildProcessError(
            'Error decoding MetaData File. Exception Message: %s', e)
