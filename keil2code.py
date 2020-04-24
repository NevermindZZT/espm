#!python
# -*- coding:UTF-8 -*-

"""
keil2code

keil mdk project to vs code wrodspace

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-18

Copyright
    (c) Letter 2020
"""
from platform.mdkproj import MdkProj
from platform.code import Code
from platform.keiltask import KeilBuildTask, KeilDownloadTask, KeilOpenTask
from manager import configmanager as cm
import sys
import argparse
import os
import espm


def initArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s version : ' + espm.VERSION, help='show the version')
    parser.add_argument('-p', '--project', type=str,
                        help='project file')
    parser.add_argument('-d', '--directory', type=str,
                        help='root directory')
    parser.add_argument('-f', '--file', type=str,
                        help='work space file') 
    parser.add_argument('-e', '--export', action='store_true', help='export task')

    return parser.parse_args()

if __name__ == "__main__":
    args = initArgs()

    if args.project:
        directory = args.directory if args.directory else "./"
        code = Code()
        proj = MdkProj(os.path.join(directory, args.project))

        code.addFolder()

        code.updateSetting("keilpath", cm.getConfig("keilpath"))
        code.updateSetting('uvprojxPath', args.project)

        packPath = os.path.join(cm.getConfig("keilpath"), "ARM/Packs")
        if not os.path.exists(packPath):
            packPath = os.path.join(cm.getConfig("keilpath"), "ARM/PACK")
        code.addLaunch(Code.JLinkLaunch(
            svdFile = os.path.join(packPath, proj.getSvdFile()),
            executable=os.path.join(
                os.path.dirname(os.path.join(directory, args.project)), 
                proj.getOutputFile()
            ),
            device=proj.getDeviceName()[:-2]
        ))
        code.addLaunch(Code.STLinkLaunch(
            svdFile = os.path.join(packPath, proj.getSvdFile()),
            executable=os.path.join(
                os.path.dirname(os.path.join(directory, args.project)),
                proj.getOutputFile()
            ),
            device=proj.getDeviceName()[:-2]
        ))

        code.addTask(KeilBuildTask(
            fileLocation=r"${workspaceFolder}"
        ))
        code.addTask(KeilDownloadTask())
        code.addTask(KeilOpenTask())
        code.addTask(KeilBuildTask(
            label='rebuild',
            rebuild=True,
            fileLocation=r"${workspaceFolder}"
        ))

        code.addRecommendations([
            "dan-c-underwood.arm",
            "ms-vscode.cpptools",
            "marus25.cortex-debug",
            "sanaajani.taskrunnercode",
            "visualstudioexptteam.vscodeintellicode",
            "slevesque.vscode-hexdump",
            "keroc.hex-fmt"
        ])

        code.save(os.path.join(directory, "project" if args.file == None else args.file),
            export=args.export,
            dir = directory)

        cProperties = Code.CProperties()
        includes = []
        for item in proj.getIncludePaths():
            if item.startswith("."):
                path = os.path.join(os.path.dirname(args.project), item)
                if os.path.exists(os.path.join(directory, path)):
                    includes.append(path)
            else:
                if os.path.exists(item):
                    includes.append(item)
        cProperties.addConfiguration(
            Code.CProperties.Configuration(
                name='stm32',
                includePath=[
                    cm.getConfig('keilpath') + "/ARM/ARMCC/**",
                    "${workspaceFolder}/**"
                ] + includes,
                defines=Code.CProperties.Configuration.getDefaultDefines()
                        + proj.getDefines()
            )
        )
        cProperties.save(directory)