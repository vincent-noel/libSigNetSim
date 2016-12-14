#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess


class MyInstall(install):

	def run(self):
		#Downloading and compiling plsa library
		subprocess.call(['git', 'clone', 'https://github.com/vincent-noel/plsa.git', 'libsignetsim/lib/plsa'])
		subprocess.call(['make', '-C', 'libsignetsim/lib/plsa', 'all'])

		#Compiling the numerical integration code
		subprocess.call(['make', '-C', 'libsignetsim/lib/integrate'])

		#Some old installs need to update distribute to install (at least) matplotlib
		subprocess.call(['easy_install', '-U', 'distribute'])

		#Installing the python dependencies
		subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

		install.do_egg_install(self)


setup(name='libsignetsim',
	  version='0.1',
	  description='An e-Science framework for mathematical modeling and computational simulation of molecular signaling networks',
	  author='Vincent Noel',
	  author_email='vincent-noel@butantan.gov.br',
	  url='',
	  packages=find_packages(),
	  include_package_data=True,
	  install_requires=['matplotlib', 'python-libsbml', 'sympy', 'numpy', 'pydstool', 'mpld3', "python-libsedml"],
	  cmdclass={'install': MyInstall}
)
