#!/usr/bin/python
# -*- coding:UTF-8 -*-

"""
config manager

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-15

Copyright
    (c) Letter 2020
"""
from manager import pathmanager
from manager import packagemanager as pm
import os
import json
import logging

configData = None

SOURCE_FILE_NAME = "packages.json"
CONFIG_FILE_NAME = "config.json"
DEFAULT_CONFIG = r"""{
    "source": "https://raw.githubusercontent.com/NevermindZZT/espm/master/data/packages.json"
}
"""

def mkConfigDir():
    configDir = os.path.dirname(pathmanager.getEspmPath(pathmanager.PATH_CONFIG))
    if not os.path.exists(configDir):
        os.mkdir(configDir)


def loadConfig():
    """
    加载配置

    Returns:
        `None`
    """
    global configData
    configFile = pathmanager.getConfigPath(CONFIG_FILE_NAME)
    mkConfigDir()
    if not os.path.isfile(configFile):
        with open(configFile, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_CONFIG)
    with open(configFile, 'r', encoding='utf-8') as f:
        configData = json.loads(f.read())


def getSource():
    """
    获取默认源

    Returns:
        str: 默认源
    """
    global configData
    sourceFile = pathmanager.getConfigPath(SOURCE_FILE_NAME)
    mkConfigDir()
    if not os.path.isfile(sourceFile):
        updateSource()
    
    return sourceFile

def updateSource(source=None):
    """
    更新源

    Args:
        source(str): 源

    Returns:
        `None`
    """
    global configData
    if source == None:
        if configData == None:
            loadConfig()
        source = configData['source']

    sourceFile = pathmanager.getConfigPath(SOURCE_FILE_NAME)
    mkConfigDir()
    packages = {"version": "v0.0.1", "name": "espm packages", "packages": []}
    if configData == None:
        loadConfig()
    logging.info("update source form %s", source)
    packages['packages'] = pm.getPackages(source)
    with open(sourceFile, 'w') as f:
        f.write(json.dumps(packages, indent=4))

def updateConfig(key, value):
    """
    更新配置项

    Args:
        key(str): key
        value(Any): value

    Returns:
        `None`
    """
    global configData
    if configData == None:
        loadConfig()
    configData[key] = value
    configFile = pathmanager.getConfigPath(CONFIG_FILE_NAME)
    with open(configFile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(configData, indent=4))

def getConfig(key):
    """
    获取配置项

    Args:
        key(str): key

    Returns:
        value
    """
    global configData
    if configData == None:
        loadConfig()
    return configData[key]
