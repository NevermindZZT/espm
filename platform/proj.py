#!/usr/bin/python
# -*- coding:UTF-8 -*-

"""
project

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-15

Copyright
    (c) Letter 2020
"""
from manager import packagemanager as pm
import os
import json

class Proj():

    def __init__(self, project):
        self._project = project
        self.initProjPackages()

    def initProjPackages(self):
        self._packagesFile = os.path.join(os.path.dirname(self._project), "packages.json")
        self._packages = {}
        if not os.path.exists(self._packagesFile):
            self._packages['version'] = "v0.0.1"
            self._packages['name'] = "espm packages"
            packages = []
            self._packages['packages'] = packages
            with open(self._packagesFile, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self._packages, ensure_ascii=False, indent=4))
        else:
            try:
                with open(self._packagesFile, 'r', encoding='utf-8') as f:
                    self._packages = json.loads(f.read())
            except:
                os.remove(self._packagesFile)
                self.initProjPackages()

    def updateSources(self, moduleName, srcs):
        """
        更新源文件

        Args:
            moduleName(str): 模块名
            srcs(list): 源文件列表

        Returns:
            `None`
        """
        pass

    def updateIncludes(self, moduleName, includes):
        """
        更新头文件路径

        Args:
            moduleName(str): 模块名
            includes(list): 头文件路径列表

        Returns:
            `None`
        """
        pass

    def removeSources(self, moduleName, srcs):
        """
        移除源文件

        Args:
            moduleName(str): 模块名
            srcs(list): 源文件列表

        Returns:
            `None`
        """
        pass

    def removeIncludes(self, moduleName, includes):
        """
        移除头文件路径

        Args:
            moduleName(str): 模块名
            includes(list): 头文件路径列表

        Returns:
            `None`
        """
        pass

    def addPackage(self, package, source=None):
        """
        添加包

        Args:
            package(str): 包

        Returns:
            `None`
        """
        if pm.install(package, source):
            self.updateSources(package, pm.getSrcs(package))
            self.updateIncludes(package, pm.getIncs(package))

            packageInfo = pm.getPackageInfo(package)
            for package in self._packages['packages']:
                if packageInfo['name'] == package['name']:
                    self._packages['packages'].remove(package)
            self._packages['packages'].append(packageInfo)
            with open(self._packagesFile, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self._packages, ensure_ascii=False, indent=4))

    def removePackage(self, package):
        """
        删除包

        Args:
            package(str): 包

        Returns:
            `None`
        """
        self.removeSources(package, pm.getSrcs(package))
        self.removeIncludes(package, pm.getIncs(package))

        packageInfo = pm.getPackageInfo(package)
        for package in self._packages['packages']:
            if packageInfo['name'] == package['name']:
                self._packages['packages'].remove(package)
        with open(self._packagesFile, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._packages, ensure_ascii=False, indent=4))

    def upgrade(self):
        """
        更新包

        Returns:
            `None`
        """
        for package in self._packages['packages']:
            self.addPackage(package['name'], self._packagesFile)