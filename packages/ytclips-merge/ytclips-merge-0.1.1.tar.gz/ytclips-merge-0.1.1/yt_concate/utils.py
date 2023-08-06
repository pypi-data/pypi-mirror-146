import os

from yt_concate.setting import CAPTIONS_DIR
from yt_concate.setting import DOWNLOADS_DIR
from yt_concate.setting import VIDEOS_DIR
from yt_concate.setting import OUTPUTS_DIR


class Utils:
    def __init__(self):
        pass

    def create_dir(self):
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(CAPTIONS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(OUTPUTS_DIR, exist_ok=True)

    def caption_file_exist(self, yt):
        path = yt.caption_filepath
        return os.path.exists(path) and os.path.getsize(path) > 0

    def video_file_exist(self, yt):
        path = yt.video_filepath
        return os.path.exists(path) and os.path.getsize(path) > 0

    def get_video_list_filepath(self, channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id)

    def video_list_file_exist(self, channel_id):
        path = self.get_video_list_filepath(channel_id)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def output_filepath(self, channel_id, search_word):
        filename = channel_id + "_" + search_word + ".mp4"
        return os.path.join(OUTPUTS_DIR, filename)
