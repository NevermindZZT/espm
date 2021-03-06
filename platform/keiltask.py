#!python
# -*- coding:UTF-8 -*-

"""
keiltask

keil task

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-18

Copyright
    (c) Letter 2020
"""
from platform.code import Code
from manager import configmanager as cm

class KeilBuildTask(Code.Task):

    def __init__(self,
                 label='build', 
                 type='shell',
                 rebuild=False,
                 fileLocation=None):
        super().__init__(label=label, 
                         type=type, 
                         command='python', 
                         args=[
                             cm.getPathConfig('keilbuild'),
                             cm.getPathConfig('keilpath') + '/UV4/UV4.exe',
                             '-r' if rebuild else '-b',
                             r"${config:uvprojxPath}"
                         ], 
                         group='build')
        self._initProblemMatcher(fileLocation)
        
    def _initProblemMatcher(self, fileLocation):
        self['problemMatcher'] = {
            "owner": "c",
            "fileLocation": [
                "relative",
                fileLocation
            ],
            "pattern": {
                "regexp": "^(.*)\\((\\d+)\\):\\s+(warning|error):\\s+#(.*):\\s+(.*)$",
                "file": 1,
                "line": 2,
                "severity": 3,
                "code": 4,
                "message": 5
            }
        }

class KeilDownloadTask(Code.Task):

    def __init__(self,
                 label='download', 
                 type='shell'):
        super().__init__(label=label, 
                         type=type, 
                         command='python', 
                         args=[
                             cm.getPathConfig('keilbuild'),
                             cm.getPathConfig('keilpath') + '/UV4/UV4.exe',
                             '-f',
                             r"${config:uvprojxPath}"
                         ], 
                         group='test')

class KeilOpenTask(Code.Task):
    
    def __init__(self,
                 label='open in keil', 
                 type='shell'):
        super().__init__(label=label, 
                         type=type, 
                         command=cm.getPathConfig('keilpath') + '/UV4/UV4.exe', 
                         args=[
                             r"${config:uvprojxPath}"
                         ], 
                         group='test')
