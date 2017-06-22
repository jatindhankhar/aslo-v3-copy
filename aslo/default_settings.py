import os


def env(variable, fallback_value=None):
    env_value = os.environ.get(variable)
    if env_value is None:
        return fallback_value
    # needed for honcho
    elif env_value == "__EMPTY__":
        return ''
    else:
        return env_value


# FLASK
DEBUG = env('DEBUG', False)
SECRET_KEY = env('SECRET_KEY', '')

# GITHUB WEBHOOK
GITHUB_HOOK_SECRET = env('GITHUB_HOOK_SECRET', '')

# CELERY
REDIS_URI = env('REDIS_URL', 'redis://localhost:6379/1')
CELERY_BROKER_URL = env('CELERY_BROKER_URL', REDIS_URI)
CELERY_TASK_IGNORE_RESULT = True

# MONGO
MONGO_DBNAME = env('MONGO_DBNAME', 'aslo')
MONGO_URI = env('MONGO_URI', 'mongodb://localhost/%s' % MONGO_DBNAME)

# BUILD
# Docker image name for activity building containers.
BUILD_DOCKER_IMAGE = env('BUILD_DOCKER_IMAGE', 'sugar-activity-build')
# Base path for cloned activities
BUILD_CLONE_REPO = env('BUILD_CLONE_REPO', '/var/tmp/activities/')
# Path where bundles are going to be stored
BUILD_BUNDLE_DIR = env('BUILD_BUNDLE_DIR', '/srv/activities/')
