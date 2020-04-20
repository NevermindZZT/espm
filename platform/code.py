#!python
# -*- coding:UTF-8 -*-

"""
code

vs code wrodspace

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-18

Copyright
    (c) Letter 2020
"""

import os
import json
from manager import configmanager

class Code():

    def __init__(self, file=None):
        if file:
            self.load(file)
        else:
            self.__data = {}
            self.init()

    def load(self, file):
        """
        加载vs code工作区

        Args:
            file(str): 工作区文件

        Returns:
            `None`
        """
        with open(file, 'r') as f:
            self.__data = json.loads(f.read())
    
    def init(self):
        """
        初始化工作区数据

        Returns:
            `None`
        """
        self.__data['folders'] = []
        self.__data['settings'] = {}
        self.__data['launch'] = {}
        self.__data['tasks'] = {}
        self.__data['extensions'] = {}
        self.__initLaunch()
        self.__initTasks()
        self.__initExtensions()

    def __initLaunch(self):
        """
        初始化调试

        Returns:
            `None`
        """
        self.__data['launch']['configurations'] = []
        self.__data['launch']['compounds'] = []

    def __initTasks(self):
        """
        初始化任务

        Returns:
            `None`
        """
        self.__data['tasks']['version'] = "2.0.0"
        self.__data['tasks']['tasks'] = []

    def __initExtensions(self):
        """
        初始化插件推荐

        Returns:
            `None`
        """
        self.__data['extensions']['recommendations'] = []
        self.__data['extensions']['unwantedRecommendations'] = []


    def addFolder(self, name=None, path='.'):
        """
        添加文件夹

        Args:
            name(str): 文件夹名
            path(str): 文件夹路径

        Returns:
            `None`
        """
        folder = {
            'path': path
        }
        if name != None:
            folder['name'] = name
        self.__data['folders'].append(folder)

    def updateSetting(self, key, value):
        """
        更新设置项

        Args:
            key(str): key
            value(Any): value

        Returns:
            `None`
        """
        self.__data['settings'][key] = value

    def addLaunch(self, launch):
        """
        添加调试项

        Args:
            launch(dict): 调试项

        Returns:
            `None`
        """
        self.__data['launch']['configurations'].append(launch)

    def addTask(self, task):
        """
        添加任务

        Args:
            task(dict): 任务

        Returns:
            `None`
        """
        self.__data['tasks']['tasks'].append(task)

    def addRecommendations(self, recommendations):
        """
        添加推荐插件

        Args:
            recommendations(str): 插件

        Returns:
            `None`
        """
        if isinstance(recommendations, str):
            self.__data['extensions']['recommendations'].append(recommendations)
        elif isinstance(recommendations, list):
            self.__data['extensions']['recommendations'] = \
                self.__data['extensions']['recommendations'] + recommendations

    def save(self, file):
        """
        保存工作区

        Args:
            file(str): 文件名

        Returns:
            `None`
        """
        with open(file + ".code-workspace", 'w') as f:
            f.write(json.dumps(self.__data, indent=4))


    class Launch(dict):

        def __init__(self,
                     name='launch',
                     cwd=r'${workspaceRoot}',
                     executable=None,
                     request='attach',
                     type='cortex-debug',
                     servertype='jlink',
                     device=None,
                     svdFile=None):
            super().__init__({
                'name': name,
                'cwd': cwd,
                'executable': executable,
                'request': request,
                'type': type,
                'servertype': servertype,
                'device': device,
                'svdFile': svdFile
            })

    class JLinkLaunch(Launch):

        def __init__(self,
                     name='launch',
                     cwd='${workspaceRoot}',
                     executable=None, 
                     request='attach', 
                     type='cortex-debug', 
                     device='STM32F407IG', 
                     svdFile=None,
                     interface='swd',
                     ipAddress=None,
                     serialNumber=None):
            super().__init__(name=name, 
                             cwd=cwd, 
                             executable=executable, 
                             request=request, 
                             type=type, 
                             servertype='jlink', 
                             device=device, 
                             svdFile=svdFile)
            self['interface'] = interface
            self['ipAddress'] = ipAddress
            self['serialNumber'] = serialNumber

    class STLinkLaunch(Launch):

        def __init__(self,
                     name='launch',
                     cwd='${workspaceRoot}',
                     executable=None, 
                     request='attach', 
                     type='cortex-debug', 
                     device='STM32F407IG', 
                     svdFile=None,
                     v1=False):
            super().__init__(name=name, 
                             cwd=cwd, 
                             executable=executable, 
                             request=request, 
                             type=type, 
                             servertype='stutil', 
                             device=device, 
                             svdFile=svdFile)
            self['v1'] = v1

    class Task(dict):

        def __init__(self,
                     label='task',
                     type='shell',
                     command=None,
                     args=[],
                     group='test'):
            super().__init__({
                'label': label,
                'type': type,
                'command': command,
                'args': args,
                'group': group
            })
        
        def _initProblemMatcher(self):
            pass
    
    class CProperties():

        def __init__(self):
            self.init()

        def init(self):
            """
            初始化

            Returns:
                `None`
            """
            self.__data = {
                "configurations": [],
                "version": 4
            }

        def addConfiguration(self, config):
            """
            添加配置

            Args:
                config(dict): 配置

            Returns:
                `None`
            """
            self.__data['configurations'].append(config)

        def save(self, dir):
            """
            保存

            Args:
                dir(str): 工作区文件夹

            Returns:
                `None`
            """
            file = os.path.join(dir, ".vscode/c_cpp_properties.json")
            if not os.path.exists(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
            with open(file, 'w') as f:
                f.write(json.dumps(self.__data, indent=4))

        class Configuration(dict):

            def __init__(self,
                         name='win32',
                         includePath=[],
                         browse=None,
                         defines=[],
                         intelliSenseMode='msvc-x64'):
                super().__init__({
                    "name": name,
                    "includePath": includePath,
                    "defines": defines,
                    "intelliSenseMode": intelliSenseMode
                })
                if browse != None:
                    self['browse'] = browse

            @classmethod
            def getDefaultDefines(cls):
                return [
                    "_DEBUG",
                    "UNICODE",
                    "__CC_ARM",
                    "uint32_t=unsigned int",
                    "uint8_t=unsigned char",
                    "uint16_t=unsigned short",
                    "__attribute__(x)="
                ]