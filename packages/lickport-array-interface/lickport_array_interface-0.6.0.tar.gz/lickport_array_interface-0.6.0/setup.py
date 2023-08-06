import pathlib
import codecs
import setuptools


here = pathlib.Path(__file__).resolve().parent

with codecs.open(here.joinpath('DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='lickport_array_interface',

    version = '0.6.0',

    description='Lickport array interface.',
    long_description=long_description,

    url='https://github.com/janelia-pypi/lickport_array_interface_python',

    author='Peter Polidoro',
    author_email='peter@polidoro.io',

    license='BSD',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
    ],

    keywords='',

    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=[
        'modular_client',
    ],
    entry_points={
        'console_scripts': [
            'lai = lickport_array_interface.lickport_array_interface:main',
        ],
    },
)
