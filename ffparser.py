#!/usr/bin/env python

import sys
import json
import argparse
import re
from pprint import pprint

from ffparser.process_utils import getoutput

ffprobe = "ffprobe -v quiet -print_format json -show_format -show_streams "


class FFprobeParser:
    def __init__(self, path):
        self.data = json.loads(getoutput(ffprobe + re.escape(path)))

        self.format = self.data["format"]
        self.audio = None
        self.video = None
        for i in range(len(self.data["streams"])):
            if self.audio is None and self.data["streams"][i]["codec_type"] == "audio":
                self.audio = self.data["streams"][i]
            if self.video is None and self.data["streams"][i]["codec_type"] == "video":
                self.video = self.data["streams"][i]

    def _get(self, option, attribute):
        if option == "audio":
            src = self.audio
        elif option == "video":
            src = self.video
        elif option == "format":
            src = self.format
        return src[attribute]

    def _getBitrate(self, option):
        if option == "audio":
            try:
                return int(self._get("audio", "bit_rate"))
            except:
                return int(self._getBitrate("format")) - int(self._getBitrate("video"))
        elif option == "video":
            try:
                return int(self._get("video", "bit_rate"))
            except:
                return int(self._getBitrate("format")) - int(self._getBitrate("audio"))
        elif option == "format":
            try:
                return int(self._get("format", "bit_rate"))
            except:
                return None

    def get(self, option, attribute):
        if attribute == "bit_rate":
            return self._getBitrate(option)
        else:
            try:
                return self._get(option, attribute)
            except:
                return None

    def pprint(self, option):
        if option == "audio":
            pprint(self.audio)
        elif option == "video":
            pprint(self.video)
        elif option == "format":
            pprint(self.format)
        else:
            pprint(self.data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="parse ffprobe's json output")

    option = parser.add_mutually_exclusive_group(required=True)
    option.add_argument("-a", "--audio", action="store_const", const="audio", dest="option", help="get audio attribute")
    option.add_argument("-v", "--video", action="store_const", const="video", dest="option", help="get video attribute")
    option.add_argument("-f", "--format", action="store_const", const="format", dest="option", help="get format attribute")

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("-g", "--get", action="store", nargs=1, dest="attribute", help="attribute name to get")
    action.add_argument("-p", "--print", action="store_true", dest="pprint", help="print all attributes and exit")

    parser.add_argument("path", action="store", nargs=1, help="path to file to parse")

    args = parser.parse_args()
    ffparser = FFprobeParser(args.path[0])
    if args.pprint:
        ffparser.pprint(args.option)
    else:
        print(ffparser.get(args.option, args.attribute[0]))
