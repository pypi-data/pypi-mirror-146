import sys
import getopt
import logging


from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_caption import DownLoadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils


def print_usage():
    print("python main.py -c <channel_id> -s <search_word> -l <limit>")
    print("python main.py --channel_id <channel_id> --search_word <search_word> --limit <limit>")
    print("options")
    print("{:>5}{:<12} ,{}".format("-c", "--channel_id", "channel id for youtube channel"))
    print("{:>5}{:<12} ,{}".format("-s", "--search_word", "search world in the channel videos"))
    print("{:>5}{:<12} ,{}".format("-l", "--limit", "integer,quantity for concatenating videos"))
    print("{:>5}{:<12} ,{}".format("", "--cleanup", "logical,delete files after the result files complete"))
    print("{:>5}{:<12} ,{}".format("", "--level", "the level to print on the screen,default is logging.INFO"))


# channel_id = "UCKSVUHI9rbbkXhvAXK-2uxA"
# search_word="incredible"


def main():
    inputs = {
        "channel_id": "",
        "search_cord": "",
        "limit": "",
        "cleanup": True,
        "level": logging.INFO,
    }
    short_opt = "hc:s:l:"
    long_opt = "help channel_id= search_word= limit= cleanup= level=".split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opt, long_opt)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', "help"):
            print_usage()
            sys.exit(0)
        elif opt in ("-c", "--channel_id"):
            inputs["channel_id"] = arg
        elif opt in ("-s", "--search_cord"):
            inputs["search_cord"] = arg
        elif opt in ("-l", "--limit"):
            inputs["limit"] = arg
        elif opt == "cleanup":
            inputs["cleanup"] = arg
        elif opt == "level":
            inputs["level"] = arg
    if not inputs["limit"].isnumeric():
        print_usage()
        sys.exit(2)
    if not inputs["cleanup"] in ("True", "true", "False", "false"):
        print_usage()
        sys.exit(2)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownLoadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("project.log")
    formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(message)s")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(inputs["level"])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == "__main__":
    main()
