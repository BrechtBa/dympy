from setuptools import setup

setup(
    name='dympy',
    version='0.0.2',
    license='GNU GENERAL PUBLIC LICENSE',
	description='A package to run Dymola commands from python in windows',
	url='https://github.com/BrechtBa/dympy',
	author='Brecht Baeten',
	author_email='brecht.baeten@gmail.com',
	packages=['dympy'],
	install_requires=['numpy','scipy'],
	classifiers = ['Programming Language :: Python :: 2.7'],
)