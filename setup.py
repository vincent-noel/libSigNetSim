#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install
from os.path import dirname, join
import subprocess

class MyInstall(install):

	def run(self):
		#Downloading and compiling plsa library
		subprocess.call(['git', 'clone', 'https://github.com/vincent-noel/plsa.git', 'libsignetsim/lib/plsa'])
		subprocess.call(['make', '-C', 'libsignetsim/lib/plsa', 'all'])

		#Compiling the numerical integration code
		subprocess.call(['make', '-C', 'libsignetsim/lib/integrate'])

		install.do_egg_install(self)

setup(name='libsignetsim',
	version=open(join(dirname(__file__), 'VERSION')).read(),
	description='An e-Science framework for mathematical modeling and computational simulation of molecular signaling networks',
	author='Vincent Noel',
	author_email='vincent-noel@butantan.gov.br',
	url='',
	packages=find_packages(),
	include_package_data=True,
	install_requires=[
		'matplotlib',
		'python-libsbml',
		'python-libnuml',
		'python-libsedml',
		'sympy',
		'numpy',
		'scipy<1.0.0',
		'pydstool',
		'mpld3',
		'jinja2',
		'bioservices',
		'pandas',
		'lxml',
		'coveralls<1.2.0'
	],
	cmdclass={'install': MyInstall}
)
