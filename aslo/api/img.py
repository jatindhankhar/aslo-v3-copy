import os
import glob
import hashlib

from flask import current_app as app
from aslo.service import activity as activity_service
from .exceptions import ReleaseError, ScreenshotDoesNotExist
from imgurpython import ImgurClient


def get_icon(repo_path, icon_name):
    icon_path = os.path.join(repo_path, 'activity', icon_name + '.svg')
    if not os.path.isfile(icon_path):
        raise ReleaseError('Icon file %s is missing' % icon_path)

    try:
        with open(icon_path, 'rb') as f:
            return f.read()
    except IOError as e:
        raise ReleaseError(
            'Failed opening icon file %s with error: %s' % (icon_path, e)
        )


def get_img_hash(img_path, blocksize=2**20):
    h = hashlib.sha1()
    with open(img_path, 'rb') as f:
        for chunk in iter(lambda: f.read(blocksize), b''):
            h.update(chunk)

    return str(h.hexdigest())


def upload_img_to_imgur(image_path):
    imgur_client = ImgurClient(
        app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_SECRET']
    )
    result = imgur_client.upload_from_path(image_path)
    return (result['link'], result['deletehash'])


def get_screenshots(repo_path, bundle_id):
    screenshots_path = os.path.join(repo_path, 'screenshots')
    if not os.path.isdir(screenshots_path):
        raise ScreenshotDoesNotExist(
            'Screenshots folder %s doesn\'t exit' % screenshots_path
        )

    old_screenshots = activity_service.get_all_screenshots(bundle_id)
    new_screenshots = {}
    for lang in os.listdir(screenshots_path):
        if not os.path.isdir(os.path.join(screenshots_path, lang)):
            continue

        new_screenshots[lang] = {}
        images = os.path.join(screenshots_path, lang, '*.*')
        for image in glob.glob(images):
            if not image.endswith('.png'):
                continue

            _hash = get_img_hash(image)
            new_screenshots[lang][_hash] = {}
            if lang in old_screenshots and _hash in old_screenshots[lang]:
                new_screenshots[lang][_hash] = old_screenshots[lang][_hash]
                continue

            link, deletehash = upload_img_to_imgur(image)
            new_screenshots[lang][_hash] = (link, deletehash)

        if len(new_screenshots[lang]) == 0:
            del new_screenshots[lang]

    return new_screenshots
