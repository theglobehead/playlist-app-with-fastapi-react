import os
from io import BytesIO
from typing import List

from flask import send_file, Response

from controllers.constants import SONG_PICTURE_PATH, DEFAULT_PROFILE_PICTURE_PATH
from models.song import Song
from utils.common_utils import CommonUtils


class ControllerSong:
    pass
