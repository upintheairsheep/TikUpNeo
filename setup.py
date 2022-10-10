from os import path
from typing import List

from setuptools import setup, find_packages

from tikup.tikup import getVersion


def read_multiline_as_list(file_path: str) -> List[str]:
    with open(file_path) as file_handler:
        contents = file_handler.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


with open('README.md', 'r') as f:
    long_description = f.read()

requirements = read_multiline_as_list("requirements.txt")

setup(
    name='tikupneo',
    version=getVersion(),
    description='An auto downloader and uploader for TikTok videos.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/upintheairsheep/TikUpNeo',
    author='upintheairsheep',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tikup = tikup.tikup:main',
        ],
    },
    python_requires='>=3.5, <4',
    install_requires=requirements,
)
