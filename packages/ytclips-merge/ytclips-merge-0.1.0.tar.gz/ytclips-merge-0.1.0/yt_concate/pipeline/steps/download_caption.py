import os
import time
import logging

from threading import Thread
from youtube_transcript_api import YouTubeTranscriptApi
from yt_concate.pipeline.steps.step import Step


class DownLoadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        start = time.time()
        for yt in data:
            logger.info("downloading caption for url", yt.id)
            if utils.caption_file_exist(yt):
                logger.info("found existing file")
                continue
            try:
                self.process_thread(data)
                threads = []
                for i in range(os.cpu_count()):
                    threads.append(Thread(target=self.process_thread))
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                with open(yt.caption_filepath, "w") as f:
                    for i in str(threads):
                        f.write(i)

            except Exception:
                logger.warning('error when downloading caption for', yt.url)
                continue
        end = time.time()
        logger.info("took", end - start, "seconds")
        return data

    def process_thread(self, data):
        for yt in data:
            YouTubeTranscriptApi.get_transcript(yt.url)
