# coding=utf8
from setuptools import setup, find_packages

__author__ = 'zhangyf'
with open('requirements.txt', 'r') as f:
    requires = [line.rstrip() for line in f.readlines()]

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version():
    u""" 从__version__.py中读取版本号。 """
    with open('jd_py_base/__version__.py') as version_file:
        for line in version_file:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

setup(
    name="jd_py_base",
    version=get_version(),
    author="zhangyf",
    author_email="zhangyf@jindefund.com",
    description="all_common_func",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "src"},
    packages=find_packages(),
    install_requires=requires,
    python_requires='>3.5',
    platforms="win_amd64"
)





