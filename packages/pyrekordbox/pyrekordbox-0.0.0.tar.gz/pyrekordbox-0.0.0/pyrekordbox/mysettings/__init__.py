# coding: utf-8
#
# This code is part of pyrekordbox.
#
# Copyright (c) 2022, Dylan Jones

import os
import re
from . import structs
from .file import MySettingFile, MySetting2File, DjmMySettingFile, DevSettingFile

RE_MYSETTING = re.compile(".*SETTING[0-9]?.DAT$")

FILES = {
    "DEVSETTING.DAT": DevSettingFile,
    "DJMMYSETTING.DAT": DjmMySettingFile,
    "MYSETTING.DAT": MySettingFile,
    "MYSETTING2.DAT": MySetting2File,
}


def get_mysetting_paths(root, deep=False):
    files = list()
    for root, _, names in os.walk(root):
        for fname in names:
            if RE_MYSETTING.match(fname):
                files.append(os.path.join(root, fname))
        if not deep:
            break
    return files


def read_mysetting_file(path):
    obj = FILES[os.path.split(path)[1]]
    return obj(path)
