import os
import logging

from yt_concate.pipeline.steps.step import Step
from yt_concate.setting import VIDEOS_DIR, CAPTIONS_DIR


class Postflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        logger.info("in postflight")
        if inputs["cleanup"] == "True":
            os.remove(VIDEOS_DIR)
            os.remove(CAPTIONS_DIR)
