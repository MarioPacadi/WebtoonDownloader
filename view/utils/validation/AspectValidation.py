import logging
import os
from pathlib import Path

import aspectlib
import validators
from validators import url

from Models.WebtoonDownloader import WebtoonsDownloader


def is_webtoon_data_valid(webtoon_data: WebtoonsDownloader | None):
    if webtoon_data is None:
        return False

    if not url(webtoon_data.starting_url):
        logging.error("Webtoon url is not valid. Aborting action.")
        return False

    if not os.path.exists(webtoon_data.folder_path):
        Path(webtoon_data.folder_path).mkdir(parents=True, exist_ok=True)
        logging.error("Webtoon folder path doesn't exist. Making folder. Continuing action.")
        # return False

    return True


@aspectlib.Aspect
def validate_webtoon(*args, **kwargs):
    webtoon_data: WebtoonsDownloader | None = args[0].frame_row1_col2.get_data()  # args[0] is self
    if not is_webtoon_data_valid(webtoon_data):
        return None  # Returning None prevents the original function from being executed
    yield aspectlib.Proceed(*args, **kwargs)
