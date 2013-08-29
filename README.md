ffparser
========

Simple python script to parse JSON output of ffprobe.

Usage:
------

  `ffparser.py [-h] (-a | -v | -f) (-g ATTRIBUTE | -p) path`

Options:
--------

```
  path                  path to file to parse
  -h, --help            show this help message and exit
  -a, --audio           get audio attribute
  -v, --video           get video attribute
  -f, --format          get format attribute
  -g ATTRIBUTE, --get ATTRIBUTE
                        attribute name to get
  -p, --print           print all attributes and exit
```

Requirements:
------------

Later version of [FFmpeg](http://www.ffmpeg.org/download.html), one that
supports json print_format

Ubuntu
------

The FFmpeg package version that is included in Ubuntu's repository is too old.
Add [Jon Severinsson's PPA repository](https://launchpad.net/~jon-severinsson/+archive/ffmpeg) to get the
latest version
