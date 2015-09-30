from setuptools import setup,find_packages

setup(
    name='dympy',
    version='0.0.1',
    license='GNU GENERAL PUBLIC LICENSE',
	description='A package to run Dymola commands from python in windows',
	url='https://github.com/BrechtBa/dympy',
	author='Brecht Baeten',
	author_email='brecht.baeten@gmail.com',
	packages=find_packages(),
	install_requires=['numpy','scipy'],
)