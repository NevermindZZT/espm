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


def initArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s version : v0.0.1', help='show the version')
    parser.add_argument('-p', '--project', type=str,
                        help='project file')
    parser.add_argument('-d', '--directory', type=str,
                        help='root directory')
    parser.add_argument('-f', '--file', type=str,
                        help='work space file')

    return parser.parse_args()

if __name__ == "__main__":
    args = initArgs()

    if args.project and args.directory:
        code = Code()
        proj = MdkProj(os.path.join(args.directory, args.project))

        code.addFolder()

        code.updateSetting("keilpath", cm.getConfig("keilpath"))
        code.updateSetting('uvprojxPath', args.project)

        code.addLaunch(Code.JLinkLaunch(
            svdFile = os.path.join(
                cm.getConfig('keilpath'),
                os.path.join("ARM/Packs", proj.getSvdFile())
            ),
            executable=os.path.join(
                os.path.dirname(os.path.join(args.directory, args.project)), 
                proj.getOutputFile()
            ),
            device=proj.getDeviceName()[:-2]
        ))
        code.addLaunch(Code.STLinkLaunch(
            svdFile = os.path.join(
               cm.getConfig('keilpath'),
                os.path.join("ARM/Packs", proj.getSvdFile())
                ),
            executable=os.path.join(
                os.path.dirname(os.path.join(args.directory, args.project)),
                proj.getOutputFile()
            ),
            device=proj.getDeviceName()[:-2]
        ))

        code.addTask(KeilBuildTask(
            fileLocation=os.path.join(r"${workspaceFolder}", os.path.dirname(args.project))
        ))
        code.addTask(KeilBuildTask(
            label='rebuild',
            rebuild=True,
            fileLocation=os.path.join(r"${workspaceFolder}", os.path.dirname(args.project))
        ))
        code.addTask(KeilDownloadTask())
        code.addTask(KeilOpenTask())

        code.addRecommendations([
            "dan-c-underwood.arm",
            "ms-vscode.cpptools",
            "marus25.cortex-debug",
            "sanaajani.taskrunnercode",
            "visualstudioexptteam.vscodeintellicode",
            "slevesque.vscode-hexdump",
            "keroc.hex-fmt"
        ])

        code.save(os.path.join(args.directory, "project" if args.file == None else args.file))

        cProperties = Code.CProperties()
        includes = []
        for item in proj.getIncludePaths():
            if item.startswith("."):
                includes.append(os.path.join(os.path.dirname(args.project), item))
            else:
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
        cProperties.save(args.directory)