from setuptools import setup, find_packages

setup(
    name='tFake PyKrita for Krita v 5.1.0-prealpha build date 15-April-2022-00_17_36',
    # version='0.1',
    version = '3.10.2',
    license='Unknown',
    author="Source code generator by scottpetrovic, modified by Olliver Aira aka officernickwilde.",
    author_email='olliver.aira@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # url='https://github.com',
    keywords='Krita intellisense autocomplete autocompletion Python PyKrita code highlight fake module',
    install_requires=[],

)
