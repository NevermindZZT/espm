#!/usr/bin/python
# -*- coding:UTF-8 -*-

"""
path manager

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-14

Copyright
    (c) Letter 2020
"""

import os

PATH_ESPM = "espm"

PATH_PACKAGES = "packages"
PATH_CONFIG = "config"

def getHome():
    return os.path.expanduser('~')

def getEspmPath(path=None):
    if path == None:
        return os.path.join(getHome(), PATH_ESPM)
    else:
        return os.path.join(os.path.join(getHome(), PATH_ESPM), path)

def getPackagePath(package):
    return os.path.join(getEspmPath(PATH_PACKAGES), package)

def getConfigPath(file):
    return os.path.join(getEspmPath(PATH_CONFIG), file)