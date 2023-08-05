import logging

from yt_concate.pipeline.steps.step import Step


class Preflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        logger.info("in preflight")
        utils.create_dir()
