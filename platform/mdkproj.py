#!/usr/bin/python
# -*- coding:UTF-8 -*-

"""
mdk project

Author
    Letter(nevermindzzt@gmail.com)

Date
    2020-04-15

Copyright
    (c) Letter 2020
"""
import xml.etree.ElementTree as ET
from platform.proj import Proj
import os

class MdkProj(Proj):

    def __init__(self, project):
        super().__init__(project)
        self.__doc = ET.parse(project)

    def updateSources(self, moduleName, srcs):
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            groupsParent = target.find("Groups")
            groups = groupsParent.findall("Group")
            for group in groups:
                name = group.find("GroupName").text
                if name == moduleName:
                    groupsParent.remove(group)

            group = ET.SubElement(groupsParent, "Group")
            groupName = ET.SubElement(group, "GroupName")
            groupName.text = moduleName
            files = ET.SubElement(group, "Files")
            for src in srcs:
                item = ET.SubElement(files, "File")
                fileName = ET.SubElement(item, "FileName")
                fileName.text = os.path.basename(src)
                fileType = ET.SubElement(item, "FileType")
                fileType.text = "1"
                filePath = ET.SubElement(item, "FilePath")
                filePath.text = src
        tree = ET.ElementTree(project)
        tree.write(self._project, xml_declaration=True)

    def updateIncludes(self, moduleName, includes):
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            incsNode = target.find("TargetOption/TargetArmAds/Cads/VariousControls/IncludePath")
            for include in includes:
                if not include in incsNode.text.split(";"):
                    incsNode.text = incsNode.text + ";" + include
        tree = ET.ElementTree(project)
        tree.write(self._project, xml_declaration=True)

    def removeSources(self, moduleName, srcs):
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            groupsParent = target.find("Groups")
            groups = groupsParent.findall("Group")
            for group in groups:
                name = group.find("GroupName").text
                if name == moduleName:
                    groupsParent.remove(group)
        
        tree = ET.ElementTree(project)
        tree.write(self._project, xml_declaration=True)

    def removeIncludes(self, moduleName, includes):
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            incsNode = target.find("TargetOption/TargetArmAds/Cads/VariousControls/IncludePath")
            incList = incsNode.text.split(";")
            for inc in incList:
                if inc in includes:
                    incList.remove(inc)
            incsNode.text = ";".join(incList)
        tree = ET.ElementTree(project)
        tree.write(self._project, xml_declaration=True)

    def getSrcDir(self):
        """
        获取所有源文件的目录

        Returns:
            
        """
        pass

    def getIncludePaths(self):
        """
        获取所有头文件路径

        Returns:
            list 头文件路径列表
        """
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            incsNode = target.find("TargetOption/TargetArmAds/Cads/VariousControls/IncludePath")
            incList = incsNode.text.split(";")
            return incList
        return None

    def getDefines(self):
        """
        获取所有全局宏

        Returns:
            list 宏列表
        """
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            defNode = target.find("TargetOption/TargetArmAds/Cads/VariousControls/Define")
            defs = defNode.text.split(",")
            return defs
        return None

    def getOutputFile(self):
        """
        获取输出文件

        Returns:
            str 输出文件
        """
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            outputDir = target.find("TargetOption/TargetCommonOption/OutputDirectory").text
            outputFileName = target.find("TargetOption/TargetCommonOption/OutputName").text
            return os.path.join(outputDir, outputFileName + ".axf")
        return None

    def getSvdFile(self):
        """
        获取SVD文件

        Returns:
            str SVD文件
        """
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            packId = target.find("TargetOption/TargetCommonOption/PackID").text
            dir = '/'.join(packId.split('.', 2))
            sfdFile = target.find("TargetOption/TargetCommonOption/SFDFile").text
            splits = sfdFile.split('$')
            return os.path.join(dir, splits[len(splits) - 1])
        return None

    def getDeviceName(self):
        """
        获取设备名

        Returns:
            str 设备名
        """
        project = self.__doc.getroot()
        targets = project.findall("Targets/Target")
        for target in targets:
            deviceName = target.find("TargetOption/TargetCommonOption/Device").text
            return deviceName
        return None