#!/usr/bin/env python
# encoding=utf-8

from .logger import *


class PipPackage:

    # 初始化
    def __init__(self):
        print_verbose(f'## Pip Package')
        print_verbose()
        if args.action[1] is ACTION_PIP_CREATE: self.create()
        elif args.action[1] is ACTION_PIP_PUBLISH: self.publish()
        elif args.action[1] is ACTION_PIP_INSTALL: self.install()


    @staticmethod
    def create():
        print_verbose(f'## create')
        print_verbose()

        print_verbose(f'### 填写包信息')
        print_verbose()

        if args.debug is False:
            print_warning('暂未实现...')
            return

        print_info(f'请输入新建包的相关信息：')
        print_info(f'1. 包名缩写（即 pip package name）：', end='')
        if args.name is not None: print(f'{args.name}')
        else: args.name = input()

        print_info(f'2. CMD（即 命令行执行时的命令名，如当前包为 {CMD}，非CLI包 可跳过）：', end='')
        args.full_name = input()

        print_info(f'3. 简单描述（可跳过）：', end='')
        args.desc = input()

        print_info(f'4. 作者（可跳过）：', end='')
        args.author = input()

        print_info(f'5. 作者邮箱（可跳过）：', end='')
        args.author_email = input()

        print_info(f'6. 个人主页（可跳过）：', end='')
        args.author_url = input()

        print_debug(f'name = {args.name}')
        print_debug(f'full_name = {args.full_name}')
        print_debug(f'desc = {args.desc}')
        print_debug(f'author = {args.author}')
        print_debug(f'author_email = {args.author_email}')
        print_debug(f'author_url = {args.author_url}')

        print_verbose(f'### 基于模板创建包')
        print_verbose()
        os_system(f'kks -f {DIR}/../package_tpl -t ~/Desktop/{args.name}')

        print_verbose(f'### 使用示例')
        print_verbose()
        cmd = f'python3 ~/Desktop/{args.name}/tests/test.py -h'
        print_info(f'使用示例：$ {cmd}')
        print_info()
        os_system(cmd)


    @staticmethod
    def publish():
        print_verbose(f'## publish')
        print_verbose()

        # 按需删除已生成文件
        os_system('rm -rf dist')

        # 构建
        os_system(f'python3 -m build')

        # 上传
        command = 'twine upload dist/*'
        if args.test:
            command = f'{command} --repository testpypi'
        os_system(command)


    @staticmethod
    def install():
        print_verbose(f'## install')
        print_verbose()

        command = f'pip3 install {args.name}'
        if args.version is not None:
            command = f'{command}=={args.version}'
        elif args.upgrade:
            command = f'{command} --upgrade'
        if args.test:
            command = f'{command} -i https://test.pypi.org/simple/'
        os_system(command)
