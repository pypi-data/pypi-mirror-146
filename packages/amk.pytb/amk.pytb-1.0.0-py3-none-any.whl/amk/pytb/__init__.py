#!/usr/bin/env python
# encoding=utf-8

from .arg_parse import *
from .logger import *
from .pip_package import PipPackage


def main():
    print_verbose()
    print_verbose(f'# Python Toolbox')
    print_verbose()
    if len(args.action) == 0: parser.print_help()
    elif args.action[0] is ACTION_PIP: PipPackage()
    else: parser.print_help()


if __name__ == '__main__':
    main()
