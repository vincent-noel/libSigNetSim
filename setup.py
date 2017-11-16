#!/usr/bin/env python

from setuptools import setup, find_packages, Extension
from setuptools.command.install import install
from os.path import dirname, join
import subprocess

class MyInstall(install):

	def run(self):
		#compiling plsa library
		subprocess.call(['make', '-C', 'libsignetsim/lib/plsa', 'all'])

		#Compiling the numerical integration code
		# subprocess.call(['make', '-C', 'libsignetsim/lib/integrate'])

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
	ext_modules=[
		Extension(
			'libsignetsim.lib.integrate.integrate',
			sources=[
				'libsignetsim/lib/integrate/src/shared.c',
				'libsignetsim/lib/integrate/src/events.c',
				'libsignetsim/lib/integrate/src/ode.c',
				'libsignetsim/lib/integrate/src/dae.c',
				'libsignetsim/lib/integrate/src/integrate.c',
				'libsignetsim/lib/integrate/src/realtype_math.c',
			]
		),
	],
	cmdclass={'install': MyInstall}
)
