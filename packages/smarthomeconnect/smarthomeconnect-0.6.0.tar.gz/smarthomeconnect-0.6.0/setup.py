#!/usr/bin/env python
# Copyright 2020-2021 Michael Thies <mail@mhthies.de>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os.path
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class custom_build_py(build_py):
    def run(self):
        subprocess.check_call(['npm', 'install'])
        subprocess.check_call(['npm', 'run', 'build'])
        super().run()


with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='smarthomeconnect',
    version='0.6.0',
    description='The Smart Home Connect home automation framework based on AsyncIO',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Michael Thies',
    author_email='mail@mhthies.de',
    url='https://github.com/mhthies/smarthomeconnect',
    cmdclass={
        'build_py': custom_build_py
    },
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    python_requires='~=3.7',
    install_requires=[
        'aiohttp>=3.6,<4',
        'jinja2>=2.11,<4',
        'MarkupSafe>=1.1,<3',
    ],
    extras_require={
        'mysql': ['aiomysql>=0.0.21,<=0.0.22'],
        'knx': ['knxdclient~=0.4.0'],
        'dmx': ['pyserial-asyncio>=0.3,<0.7'],
        'midi': ['mido>=1.2.9,<2', 'python-rtmidi>=1.4.6,<2'],
        'mqtt': ['paho-mqtt>=1.5.1,<2', 'asyncio-mqtt>=0.10.0,<0.13'],
        'pulse': ['pulsectl_asyncio~=0.2.0'],
        'telegram': ['aiogram~=2.18'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Home Automation',
        'Framework :: AsyncIO',
    ],
)
