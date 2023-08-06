#!/usr/bin/env python3

import setuptools
# my_math = setuptools.Extension("joby_m_anthony_iii.math",
	# sources=["joby_m_anthony_iii/math/math.cpp"]
# )
# import skbuild

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	# skbuild.setup(
	name = "joby_m_anthony_iii",
	version = "1.6.6.1",
	author = "Joby M. Anthony III",
	author_email = "jmanthony1@liberty.edu",
	description = "Numerical methods/techniques.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url = "https://github.com/jmanthony3/joby_m_anthony_iii.git",
	# setuptools.find_packages(),
	packages = [
		"joby_m_anthony_iii"
	],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	platforms = "any",
	# ext_modules = [my_math],
	install_requires = [
	],
	# setup_requires = [
	# 	'setuptools_scm',
	# ],
	tests_requires = [
	],
	cmake_args = [
		# we can safely pass OSX_DEPLOYMENT_TARGET as it's ignored on
		# everything not OS X. We depend on C++11, which makes our minimum
		# supported OS X release 10.9
		'-DCMAKE_OSX_DEPLOYMENT_TARGET=10.9',
	],
	use_scm_version = True,
)