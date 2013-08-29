#!/usr/bin/env python

import json
import re
from pprint import pprint

from ffparser.process_utils import getoutput

import pdb

PROBE_COMMAND = "ffprobe -v quiet -print_format json -show_format -show_streams "

class FFprobeParser:

    def __init__(self, path):
        self.data = json.loads(getoutput(PROBE_COMMAND + re.escape(path)))

        self.format = self.data["format"]
        self.audio = None
        self.video = None

        for i in range(len(self.data["streams"])):
            if self.audio is None and self.data["streams"][i]["codec_type"] == "audio":
                self.audio = self.data["streams"][i]
            if self.video is None and self.data["streams"][i]["codec_type"] == "video":
                self.video = self.data["streams"][i]

    def _get(self, option, attribute):
        src = getattr(self, option)
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

    def pprint(self, option='data'):
        pprint(getattr(self, option))
