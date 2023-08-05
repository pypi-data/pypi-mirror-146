import ast

from yt_concate.pipeline.steps.step import Step


class ReadCaption(Step):
    def process(self, data, inputs, utils):
        for yt in data:
            if not utils.caption_file_exist(yt):
                continue

            with open(yt.caption_filepath, "r") as f:
                captions = {}
                data_file = ast.literal_eval(f.read())
                for line in data_file:
                    caption = line['text']
                    time = str(line["start"]) + "-->" + str(line["duration"])
                    captions[caption] = time
            yt.captions = captions
        return data
