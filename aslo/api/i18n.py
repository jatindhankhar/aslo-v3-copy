import os
import glob
import polib
from aslo.celery_app import logger
from .exceptions import ReleaseError


def get_language_code(filepath):
    basename = os.path.basename(filepath)
    return os.path.splitext(basename)[0]


def get_translations(repo_path):
    logger.info('Getting translations.')
    po_files_location = os.path.join(repo_path, 'po/')

    translations = {}
    matched_files = glob.glob(os.path.join(po_files_location, '*.po'))
    if len(matched_files) == 0:
        # If no po files are found just continue working
        return translations

    po_files = list(map(polib.pofile, matched_files))
    language_codes = list(map(get_language_code, matched_files))

    # Intialize the dictionary
    for language_code in language_codes:
        translations[language_code] = {}

    for po_file, language_code in zip(po_files, language_codes):
        for entry in po_file.translated_entries():
            translations[language_code][entry.msgid] = entry.msgstr

    return translations


def translate_field(field_value, translations):
    d = {}
    for language_code in translations:
        if field_value in translations[language_code]:
            d[language_code] = translations[language_code][field_value]
    return d
