# -*- coding: utf-8 -*-
# Copyright (C) 2019 Davide Gessa

from setuptools import find_packages
from setuptools import setup
from tezpie import config

setup(name=config.NAME,
	version=config.VERSION,
	description='',
	author=['Davide Gessa'],
	setup_requires='setuptools',
	author_email=['gessadavide@gmail.com'],
	packages=[
		'tezpie',
		'tezpie.p2p',
		'tezpie.p2p.messages',
		'tezpie.proto',
		'tezpie.storage',
		'tezpie.crypto',
		'tezpie.rpc',
		'tezpie.chain'
	],
	entry_points={
		'console_scripts': [
			'tezpie=tezpie.main:start'
		],
	},
	install_requires=open ('requirements.txt', 'r').read ().split ('\n')
)
