#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import threading
import sys

runing = True

def readfile(logfile, path):
    with open(logfile, 'wb') as f:
        pass
    with open(logfile, 'rb') as f:
        while runing:
            try:
                data = f.read()
                output = None
                if len(data) == 0:
                    continue
                try:
                    output = data.decode("utf-8")
                except:
                    try:
                        output = data.decode("gbk")
                    except:
                        pass
                if output != None:
                    lines = output.split("\r\n")
                    if len(lines) > 0:
                        for line in lines:
                            if len(line) > 0:
                                line = line.replace('\\', '/')
                                if line.startswith("../") or line.startswith("./"):
                                    line = path + "/" + line
                                print(line)
            except:
                pass

if __name__ == '__main__':
    modulePath = os.path.abspath(os.curdir)
    logfile = modulePath + '/build.log'
    cmd = '\"D:/Program Files (x86)/keil/UV4/UV4.exe\" '
    for i in range(1, len(sys.argv)):
        cmd += sys.argv[i] + ' '
    cmd += '-j0 -o ' + logfile
    thread = threading.Thread(target=readfile, args=(logfile, os.path.dirname(sys.argv[3])))
    thread.start()
    code = os.system(cmd)
    runing = False
    thread.join()
    sys.exit(code)