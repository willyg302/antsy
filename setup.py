try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

import antsy

setup(
	name='antsy',
	author='William Gaul',
	author_email='willyg302@gmail.com',
	version=antsy.__version__,
	url='https://github.com/willyg302/antsy',
	license='MIT',
	py_modules=['antsy'],
	include_package_data=True,
	description='Sweet interpolated ANSI strings',
	test_suite='test',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.4',
	],
)
