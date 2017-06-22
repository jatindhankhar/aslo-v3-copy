import os
import shutil
import configparser
from flask import current_app as app
from aslo.celery_app import logger
from subprocess import call
from .exceptions import BuildProcessError


def get_repo_location(name):
    return os.path.join(app.config['BUILD_CLONE_REPO'], name)


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
        parser = configparser.ConfigParser()
        if len(parser.read(activity_file)) == 0:
            raise BuildProcessError('Error parsing metadata file')

        try:
            attributes = dict(parser.items('Activity'))
        except configparser.NoSectionError as e:
            raise BuildProcessError(
                'Error parsing metadata file. Exception message: %s', e
            )

        return attributes

    activity_file = metadata_file_exists()
    return parse_metadata_file()


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

    def clean():
        shutil.rmtree(get_repo_location(name))

    volume = get_repo_location(name) + ':/activity'
    docker_image = app.config['BUILD_DOCKER_IMAGE']
    docker_cmd = ['docker', 'run', '--rm', '-v', volume, docker_image]
    logger.info('Running docker command: "%s"', ' '.join(docker_cmd))
    if call(docker_cmd) != 0:
        raise BuildProcessError('Docker building process has failed')

    store_bundle()
    clean()
