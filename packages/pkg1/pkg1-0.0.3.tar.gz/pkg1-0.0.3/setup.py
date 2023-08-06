'''
@file : setup.py
@Time : 15/4/2022 上午8:24
@Author： Zheng Xingyu
@Version：1.0
@Contact：zhengxingyu_1990@126.com
'''

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'pkg1'
DESCRIPTION = 'A daily useful kit by Hong Peng.'
URL = 'https://github.com/zhengxingyu/hpkit.git'
EMAIL = 'zhengxingyu_1990@126.com'
AUTHOR = 'zhengxingyu'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.3'

# What packages are required for this module to be executed?
REQUIRED = ["numpy", "matplotlib"]

# Setting.
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    license="MIT"
)