# Author: Lachlan Whyborn
# Last Modified: Mon 22 Jul 2024 04:14:34 PM AEST

from setuptools import setup

setup(
    name = 'cablerun_test',
    version = '0.1',
    description = 'a test package',
    author = 'me',
    entry_points = {
        'console_scripts': ['cablerun=cablerun.cli:cli'],
    }
)
