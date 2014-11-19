#!/usr/bin/env python
#coding:utf-8


from setuptools import setup

setup(  name='Alarmer',
        version='1.0.2',
        description='Python Alarm Utilities',
        author='Dmitry Vysochin',
        author_email='dmitry.vysochin@gmail.com',
        url='https://github.com/veryevilzed/alarmer',
        packages=['alarmer', 'alarmer.plugins'],
        package_dir={'alarmer': 'src/alarmer', 'alarmer.plugins': 'src/alarmer/plugins'},
        #package_data={'alarmer': ['data/*.dat']},
        install_requires=(
                'configparser',
                'requests',
                'python-simple-hipchat',
            ),
        entry_points = {
            'console_scripts': ['alarmer=alarmer.alarm:main', ],
        }
     )