#!/usr/bin/env python

from setuptools import setup, find_packages, Extension
from os.path import dirname, join

setup(name='libsignetsim',
	version=open(join(dirname(__file__), 'VERSION')).read(),
	description='Python library designed for building, adjusting and analyzing quantitative biological models.',
	author='Vincent Noel',
	author_email='contact@vincent-noel.fr',
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
		Extension(
			'libsignetsim.lib.plsa.libplsa-serial',
			sources=[
				'libsignetsim/lib/plsa/src/config.c',
				'libsignetsim/lib/plsa/src/error.c',
				'libsignetsim/lib/plsa/src/distributions.c',
				'libsignetsim/lib/plsa/src/random.c',
				'libsignetsim/lib/plsa/src/plsa.c',
				'libsignetsim/lib/plsa/src/lsa.c',
				'libsignetsim/lib/plsa/src/moves.c',
				'libsignetsim/lib/plsa/src/state.c',
				'libsignetsim/lib/plsa/src/score.c',
			]
		),
		Extension(
			'libsignetsim.lib.plsa.libplsa-parallel',
			sources=[
				'libsignetsim/lib/plsa/src/config.c',
				'libsignetsim/lib/plsa/src/error.c',
				'libsignetsim/lib/plsa/src/distributions.c',
				'libsignetsim/lib/plsa/src/random.c',
				'libsignetsim/lib/plsa/src/plsa.c',
				'libsignetsim/lib/plsa/src/lsa.c',
				'libsignetsim/lib/plsa/src/moves.c',
				'libsignetsim/lib/plsa/src/state.c',
				'libsignetsim/lib/plsa/src/score.c',
				'libsignetsim/lib/plsa/src/mixing.c',
				'libsignetsim/lib/plsa/src/tuning.c',
			],
			include_dirs=[
				"/usr/lib/openmpi/include/openmpi/opal/mca/event/libevent2021/libevent",
				"/usr/lib/openmpi/include/openmpi/opal/mca/event/libevent2021/libevent/include",
				"/usr/lib/openmpi/include",
				"/usr/lib/openmpi/include/openmpi",
				"/usr/lib/x86_64-linux-gnu/openmpi/include/openmpi/opal/mca/event/libevent2021/libevent",
				"/usr/lib/x86_64-linux-gnu/openmpi/include/openmpi/opal/mca/event/libevent2021/libevent/include",
				"/usr/lib/x86_64-linux-gnu/openmpi/include",
				"/usr/lib/x86_64-linux-gnu/openmpi/include/openmpi",
			],
			define_macros=[("MPI", None)],
			extra_compile_args=["-pthread"]
		)
	],
)
