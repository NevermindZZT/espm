#!/usr/bin/python
# -*- coding:UTF-8 -*-

"""
package manager

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-14

Copyright
    (c) Letter 2020
"""

import requests
import json
import os
import shutil
from manager import pathmanager, configmanager
import logging
import subprocess

def listPackages():
    """
    列出所有已安装的包

    Returns:
        `None`
    """
    print("packages list:")
    packagesDir = pathmanager.getEspmPath(pathmanager.PATH_PACKAGES)
    names = os.listdir(packagesDir)
    for name in names:
        packageInfo = getPackageInfo(name)
        version = packageInfo['version'] if packageInfo  else "unknow"
        print("%-24s    %s"%(name, version))

def install(packageName, source=None):
    """
    安装包

    Args:
        packageName(str): 包名
        source(str): 指定源

    Returns:
        bool 安装是否成功
    """
    package = search(packageName, source)
    if package != None:
        if package['type'] == 'git':
            return clonePackageFromGit(package['url'], 
                    pathmanager.getPackagePath(packageName))
        if package['type'] == 'svn':
            return clonePackageFromSvn(package['url'], 
                    pathmanager.getPackagePath(packageName))

def uninstall(packageName):
    """
    删除包

    Args:
        packageName(str): 包名

    Returns:
        bool 删除是否成功
    """
    try:
        logging.debug("delete dir: %s"%(pathmanager.getPackagePath(packageName)))
        shutil.rmtree(pathmanager.getPackagePath(packageName))
        return True
    except:
        return False

def search(packageName, source=None):
    """
    搜索包

    Args:
        packageName(str): 包名
        source(str): 指定源

    Returns:
        package 搜索到的包, 若未找到包, 返回`None`
    """
    if source == None:
        source = configmanager.getSource()
    packages = getPackages(source)
    if packages != None:
        for item in packages:
            if item['name'] == packageName:
                return item
    return None

def getPackageInfo(packageName):
    """
    获取包信息

    Args:
        packageName(str): 包名

    Returns:
        包信息
    """
    packageInfo = None
    packagesDir = pathmanager.getEspmPath(pathmanager.PATH_PACKAGES)
    names = os.listdir(packagesDir)
    for name in names:
        if name == packageName:
            espmFlie = os.path.join(pathmanager.getPackagePath(name), "espm.json")
            if os.path.isfile(espmFlie):
                with open(espmFlie, 'r') as f:
                    packageInfo = json.loads(f.read())
            
            package = search(packageName)
            if packageInfo == None:
                packageInfo = package

            if not 'src' in packageInfo and 'src' in package:
                packageInfo['src'] = package['src']
            if not 'inc' in packageInfo and 'inc' in package:
                packageInfo['inc'] = package['inc']
            if not 'version' in packageInfo:
                packageInfo['version'] = "unknow" if not 'version' in package else package['version']

    return packageInfo
                        

def getPackages(source=None):
    """
    获取包列表

    Args:
        source(str): 源

    Returns:
        packages: 获取到的包列表, 若未找到包, 返回`None`
    """
    if source == None:
        source = configmanager.getSource()
    sourceInfo = None
    packages = None
    if source.startswith("http"):
        try:
            headers={"User-Agent": "Microsoft-WNS/10.0"}
            res = requests.get(source, headers=headers)
            if res.status_code == 200:
                sourceInfo = res.json()
        except Exception as e:
            logging.exception(e)
    elif os.path.isfile(source):
        with open(source, 'r') as f:
            sourceInfo = json.loads(f.read())
    
    if sourceInfo:
        if 'packages' in sourceInfo:
            packages = sourceInfo['packages']

        if 'sources' in sourceInfo:
            for item in sourceInfo['sources']:
                packages = packages + getPackages[item]

    return packages

def clonePackageFromGit(url, dest):
    """
    从git克隆包

    Args:
        url(str): 包地址
        dest(str): 保存包的路径

    Returns:
        bool 是否克隆成功
    """
    if os.path.isdir(os.path.join(dest, ".git")):
        logging.debug("check %s form git"%url)
        return subprocess.check_call("git pull", shell=True, cwd = dest) == 0
    else:
        logging.debug("clone %s from git"%url)
        cmd = "git clone %s %s"%(url, dest)
        return subprocess.check_call(cmd, shell=True) == 0

def clonePackageFromSvn(url, dest):
    """
    从svn克隆包

    Args:
        url(str): 包地址
        dest(str): 保存包的路径

    Returns:
        bool 是否克隆成功
    """
    logging.debug("checkout %s form svn"%url)
    cmd = "svn checkout %s %s"%(url, dest)
    return subprocess.check_call(cmd, shell=True) == 0

def getSrcs(packageName):
    """
    获取包源文件列表

    Args:
        packageName(str): 包名

    Returns:
        list: 源文件列表
    """
    packageInfo = getPackageInfo(packageName)
    srcs = []
    if packageInfo != None:
        if 'src' in packageInfo:
            for item in packageInfo['src']:
                path = os.path.join(pathmanager.getPackagePath(packageName), item)
                if os.path.isdir(path):
                    for src in os.listdir(path):
                        if src.endswith(".c"):
                            srcs.append(os.path.join(path, src))
                elif os.path.isfile(item) and item.endswith(".c"):
                    srcs.append(item)
    return srcs

def getIncs(packageName):
    """
    获取包头文件目录列表

    Args:
        packageName(str): 包名

    Returns:
        list: 头文件目录列表
    """
    packageInfo = getPackageInfo(packageName)
    incs = []
    if packageInfo != None:
        if 'inc' in packageInfo:
            for item in packageInfo['inc']:
                path = os.path.join(pathmanager.getPackagePath(packageName), item)
                if os.path.isdir(path):
                    incs.append(path)
    return incs
