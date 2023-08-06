import os
import logging

from pytube import YouTube
from threading import Thread
from yt_concate.pipeline.steps.step import Step
from yt_concate.setting import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        yt_set = set([found.yt for found in data])
        logger.info('video to download', len(yt_set))
        for yt in yt_set:
            url = yt.url
            if utils.video_file_exist(yt):
                logger.info(f"found existing video file:{url},skipping")
                continue
            logger.info("downloading", url)

            self.process_thread(data)
            threads = []
            for i in range(os.cpu_count()):
                threads.append(Thread(target=self.process_thread))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        return data

    def process_thread(self, data):
        for yt in data:
            YouTube(yt.url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id + ".mp4")
