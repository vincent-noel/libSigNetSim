#!/usr/bin/env python

from setuptools import find_packages
from distutils.core import setup, Extension
from os.path import dirname, join
from subprocess import Popen, PIPE


def get_openmpi_include_dirs():
	process = Popen("mpicc --showme:compile".split(), stdout=PIPE)
	output, error = process.communicate()

	print("Output: %s" % output)

	dirs = []
	for include_dir in output.decode().split():
		if include_dir.startswith("-I"):
			dirs.append(include_dir[2:])

	print("> Found openmpi include dirs : %s" % str(dirs))
	return dirs


setup(name='libsignetsim',
	version=open(join(dirname(__file__), 'VERSION')).read(),
	description='A library designed for building, adjusting and analyzing quantitative biological models. ',
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
		'sympy<1.2',
		'numpy',
		'scipy',
		'pydstool',
		'jinja2',
		'bioservices',
		'lxml',
		'coveralls',
		'future'
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
			],
			include_dirs=[
				"/usr/include/cvode/",
				"/usr/include/ida/",
				"/usr/include/nvector"
				"/usr/include/sundials",
			],
			libraries=['sundials_cvode', 'sundials_nvecserial', 'sundials_ida', 'm', 'lapack', 'atlas', 'blas'],
			library_dirs=['/usr/lib64/atlas-basic/'],
			define_macros=(
				[("SUNDIALS3", None)] if "SUNDIALS_VERSION_MAJOR 3" in open("/usr/include/sundials/sundials_config.h").read() else None
			),
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
			include_dirs=get_openmpi_include_dirs(),
			define_macros=[("MPI", None)],
			extra_compile_args=["-pthread"]
		)
	],
)
