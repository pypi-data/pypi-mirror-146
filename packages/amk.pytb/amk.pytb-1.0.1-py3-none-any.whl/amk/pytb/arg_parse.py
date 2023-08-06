#!/usr/bin/env python
# encoding=utf-8

import argparse
import textwrap
from .consts import *


# 命令行参数解析
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    prog=NAME,
    prefix_chars='-+',
    description=textwrap.dedent(
        f'{NAME} —— {DESC}'
        + f'\n' + '-' * 80
        + f'\nSHORTCUT: {SHORTCUT}'
        + f'\nVERSION: {VERSION}'
        + f'\nUPDATE_TIME: {UPDATE_TIME}'
        + f'\nAUTHOR_NAME: {AUTHOR_NAME}'
        + f'\nAUTHOR_EMAIL: {AUTHOR_EMAIL}'
        + f'\nAUTHOR_URL: {AUTHOR_URL}'
        + f'\nGIT_URL: {GIT_URL}'
        + f'\nPIP_URL: {PIP_URL}'
        + f'\n' + '=' * 80
    ),
)

# 一级参数
parser.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
parser.add_argument('-v', '--verbose', action='store_true', help='显示详细日志')
parser.add_argument('-V', '--version', action='version', version=VERSION, help='查看当前版本号')
parser.set_defaults(action=())

# 二级命令：pip
ACTION_PIP = 'pip'
subparsers = parser.add_subparsers(title='pip package')
# 二级命令：pip - create
ACTION_PIP_CREATE = 'create'
subparser_pip_create = subparsers.add_parser('create', help='创建 package')
subparser_pip_create.set_defaults(action=(ACTION_PIP, ACTION_PIP_CREATE))
subparser_pip_create.add_argument('name', nargs="?", help='package 名称')
subparser_pip_create.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
subparser_pip_create.add_argument('-v', '--verbose', action='store_true', help='显示详细日志')

# 二级命令：pip - publish
ACTION_PIP_PUBLISH = 'publish'
subparser_pip_publish = subparsers.add_parser('publish', help='上传 package')
subparser_pip_publish.set_defaults(action=(ACTION_PIP, ACTION_PIP_PUBLISH))
subparser_pip_publish.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
subparser_pip_publish.add_argument('-v', '--verbose', action='store_true', help='显示详细日志')
subparser_pip_publish.add_argument('-t', '--test', action='store_true', help='作为测试包进行处理')
# 二级命令：pip - install
ACTION_PIP_INSTALL = 'install'
subparser_pip_install = subparsers.add_parser('install', help='安装 package')
subparser_pip_install.set_defaults(action=(ACTION_PIP, ACTION_PIP_INSTALL))
subparser_pip_install.add_argument('name', help='package 名称')
subparser_pip_install.add_argument('version', nargs="?", help='package 版本')
subparser_pip_install.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
subparser_pip_install.add_argument('-v', '--verbose', action='store_true', help='显示详细日志')
subparser_pip_install.add_argument('-t', '--test', action='store_true', help='作为测试包进行处理')
subparser_pip_install.add_argument('-u', '--upgrade', action='store_true', help='升级到最新版本')

# 解析命令
args = parser.parse_args()
