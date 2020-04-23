#!python
# -*- coding:UTF-8 -*-

"""
espm

embedded system package manager

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-14

Copyright
    (c) Letter 2020
"""

import argparse
from manager import packagemanager as pm
from manager import configmanager as cm
from platform.mdkproj import MdkProj
import logging

VERSION = "v0.0.2"

def initArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s version : ' + VERSION, help='show the version')
    parser.add_argument('-p', '--project', type=str, dest='project',
                        help='project file')
    parser.add_argument('-update', '--update', action='store_true',
                        help='update source')
    parser.add_argument('-upgrade', '--upgrade', action='store_true',
                        help='upgrade project')
    parser.add_argument('-s', '--source', type=str,
                        help='package list source')
    parser.add_argument('-c', '--config', nargs='+',
                        help='get or set config')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', action='store_true', help='list all packages')
    group.add_argument('-i', '--install', type=str,
                       help='install package')
    group.add_argument('-u', '--uninstall', type=str,
                       help='uninstall package')
    group.add_argument('-r', '--remove', type=str,
                       help='remove package from project')
    group.add_argument('-a', '--add', type=str,
                       help='add package to project')

    return parser.parse_args()

if __name__ == "__main__":
    args = initArgs()

    logging.basicConfig(level=logging.INFO,  
                        format='[%(asctime)s %(levelname)s] %(message)s',  
                        datefmt='%d %b %Y %H:%M:%S')  

    if args.update:
        cm.updateSource(args.source)
    elif args.upgrade:
        if args.project:
            proj = None
            if args.project.endswith(".uvprojx"):
                proj = MdkProj(args.project)
            if proj != None:
                proj.upgrade()
    elif args.config:
        if len(args.config) == 1:
            print("config %s: %s"%(args.config[0], str(cm.getConfig(args.config[0]))))
        elif len(args.config) > 1:
            cm.updateConfig(args.config[0], args.config[1])
    elif args.list:
        pm.listPackages()
    elif args.install:
        if pm.install(args.install, args.source):
            logging.info("install package: %s success"%args.install)
        else:
            logging.error("install package: %s fail"%args.install)
    elif args.uninstall:
        if pm.uninstall(args.uninstall):
            logging.info("remove package: %s success"%args.uninstall)
        else:
            logging.error("remove package: %s fail"%args.uninstall)
    elif args.add:
        if args.project:
            proj = None
            if args.project.endswith(".uvprojx"):
                proj = MdkProj(args.project)
            if proj != None:
                proj.addPackage(args.add, args.source)
    elif args.remove:
        if args.project:
            proj = None
            if args.project.endswith(".uvprojx"):
                proj = MdkProj(args.project)
            if proj != None:
                proj.removePackage(args.remove)
