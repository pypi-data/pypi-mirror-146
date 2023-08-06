#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 10:36 AM
# @Author  : chenDing
from setuptools import setup
import re
import ssl
import sys
import os

if sys.argv[-1].lower() in ("submit", "publish"):
    os.system("python setup.py bdist_wheel sdist upload")
    sys.exit()

ssl._create_default_https_context = ssl._create_unverified_context
with open("readme.md", "r") as fh:
    long_description = fh.read()


def get_version():
    version = ''
    with open('mlogs/__init__.py', 'r') as fd:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fd:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    return version


__version__ = get_version()

"""
1 setup_tool.find_packages 本质是返回一个列表。所以，可以手动指定
2 没有被写入的包，不会被包装进去。
"""

packages = [
    'mlogs',
    'mlogs/third_party/notifiers/notifiers',
    'mlogs/third_party/notifiers/notifiers/providers',
    'mlogs/third_party/notifiers/notifiers/utils',
    'mlogs/third_party/notifiers/notifiers/utils/schema',
    'mlogs/third_party/notifiers/notifiers_cli',
    'mlogs/third_party/notifiers/notifiers_cli/utils',
]

setup(
    name='mlogs',
    version=__version__,
    license='Apache 2.0',
    description='loguru packaging log tools',
    packages=packages,
    author='Caturbhuja Das',
    author_email='caturbhuja@foxmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    install_requires=[
        'loguru>=0.6.0',
        'numpy>=1.19.0',
        # 'notifiers>=1.2.0',
        # notifiers 需要包如下
        "jsonschema==4.4.0",
        "requests==2.27.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
