#!/usr/bin/env python

from distutils.core import setup
import shutil

setup(
    author="Jakub Klinkovský",
    author_email="kuba.klinkovsky@gmail.com",
    name="ffparser",
    version="0.1",
    license="GPLv3",
    description="ffparser - parse ffprobe output",
    long_description=open("README.rst").read(),
    url="http://github.com/lahwaacz/ffparser",

    packages=["ffparser"],
    package_dir={"ffparser": "ffparser/"},
)

# cleanup: remove build/
shutil.rmtree("build/", ignore_errors=True)
