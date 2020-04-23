# ESPM (Embedded System Package Manager)

![version](https://img.shields.io/badge/version-0.0.2-brightgreen.svg)
![build](https://img.shields.io/badge/build-2020.04.16-brightgreen.svg)
![build](https://img.shields.io/badge/license-MIT-brightgreen.svg)

Embedded System Package Manager(嵌入式系统包管理工具) 是一个用于嵌入式系统开发情况，对各种通用模块(软件包)进行管理的工具

ESPM支持软件包的添加，更新，删除，支持git和svn，支持对嵌入式系统的工程进行修改，添加，更新，删除对应的软件包(目前仅支持MDK)

- [ESPM (Embedded System Package Manager)](#espm-embedded-system-package-manager)
  - [功能说明](#功能说明)
  - [使用](#使用)
  - [源](#源)
  - [软件包](#软件包)
  - [添加软件包](#添加软件包)
  - [keil2Code](#keil2code)

## 功能说明

- 软件源管理

  - 支持本地源，在线源

- 软件包管理

  - 添加软件包
  - 更新软件包
  - 删除软件包
  - 支持Git和Svn

- 工程修改

  - 添加软件包到工程
  - 更新工程内的软件包
  - 删除工程内的软件包
  - 支持Keil MDK5

## 使用

ESPM运行依赖于python3，请确保PC已经具备python3环境，同时，ESPM下载软件包会使用到Git或者Svn，需要视软件包来源安装Git或者Svn，并配置到环境变量

- 获取ESPM

    ```sh
    git clone https://github.com/NevermindZZT/espm
    ```

- 更新源

    从默认源地址更新源

    ```sh
    python espm.py -update
    ```

    指定源地址更新源(本地源文件或者网络地址)

    ```sh
    python espm.py -update -s https://raw.githubusercontent.com/NevermindZZT/espm/master/data/packages.json
    ```

- 获取软件包

    ```sh
    python espm.py -i letter-shell
    ```

- 删除软件包

    ```sh
    python espm.py -u letter-shell
    ```

- 添加软件包到工程

    ```sh
    python espm.py -a letter-shell -p project.uvprojx
    ```

- 删除工程内的软件包

    ```sh
    python espm.py -r letter-shell -p project.uvprojx
    ```

- 更新工程内的软件包

    ```sh
    python espm.py -upgrade -p project.uvprojx
    ```

- 列出已安装的工具包

    ```sh
    python espm.py -l
    ```

## 源

ESPM的源是一个json格式的文件，支持在线源和本地源，源内容如下：

```json
{
    "version": "v0.0.1",
    "name": "espm packages",
    "packages": [
        {
            "name": "letter-shell",
            "url": "https://github.com/NevermindZZT/letter-shell",
            "type": "git",
            "src": [
                "src"
            ],
            "inc": [
                "src"
            ]
        }
    ],
    "sources": [
        "D:/espm/localpackages.json"
    ]
}
```

`version`和`name`字段皆为固定字段，不需要关注

`packages`是软件包列表，列表中每一项都表示一个软件包，其中字段表示信息如下：

| 字段 | 信息                   | 备注           |
| ---- | ---------------------- | -------------- |
| name | 软件包名               |                |
| url  | 软件包链接             |                |
| type | 软件包类型             | "git"或者"svn" |
| src  | 软件包中源文件路径     | 目录或者文件   |
| inc  | 软件包中头文件包含目录 | 目录           |

`sources`表示源列表，可以添加本地源或者在线源

## 软件包

ESPM软件包是一个通过git或者svn进行管理的项目，已有的项目可以不进行任何更改，只需要将项目添加到软件包源中，即可通过ESPM进行管理

当然，为了方便管理，建议在软件包根目录中添加`espm.json`文件，文件内容如下：

```json
{
    "name": "letter-shell",
    "url": "https://github.com/NevermindZZT/letter-shell",
    "type": "git",
    "src": [
        "src"
    ],
    "inc": [
        "src"
    ],
    "version": "3.0.0"
}
```

`espm.json`中的内容同软件包源中的`packages`子项一致，只多了一个`version`字段，表示软件包的版本

## 添加软件包

你可以通过Pull Request，修改./data/packages.json，添加你的软件包到ESPM默认源

当然，你也可以自己新建一个软件包源文件，添加你的软件包，然后通过`python espm.py -upate`更新源，如果你想同时使用多个源，只需要在源文件的`source`中添加其他源的url即可

## keil2Code

ESPM提供了一个工具，可以将keil工程配置到VS Code，通过VS Code调用keil进行编译调试，将VS Code作为keil的外部编辑器

1. 安装arm gcc

    下载arm gcc安装并配置好环境变量，使用VS Code进行调试需要用到

2. 配置环境

    配置keil安装路径

    ```sh
    python espm.py -c keilpath "D:/Program Files (x86)/keil"
    ```

    配置编译脚本路径(位于./scripts/keilbuild.py)

    ```sh
    python espm.py -c keilbuild E:/espm/scripts/keilbuild.py
    ```

3. 导出keil工程到VS Code工作区

    可以选择以绝对路径方式或者相对路径方式导出工作区

    ```sh
    python keil2code.py -d E:/MDK_project/keilproject -p MDK-ARM/project.uvprojx
    ```

    其中，`-d`参数表示工程目录，`-p`参数表示keil工程文件遂于工程目录的相对路径

    或者使用相对路径方式

    ```sh
    cd E:/MDK_project/keilproject
    python keil2code.py -p MDK-ARM/project.uvprojx
    ```

    增加`-e`参数，可以将VS Code的任务从工作区文件中导出到工作目录

4. 打开工程

    打开工程目录下的VS Code工作区文件，根据插件推荐安装必要的插件
