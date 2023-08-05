from setuptools import setup, find_packages
from distutils.command.install import install as _install
from distutils.core import setup, Extension

module_cfuncs = Extension('mg_tok.libcfunctions',
                          sources = ['mg_tok/cfunctions.c'])

setup(
    name='mult-tokenizer',
    version='0.1.3',
    url='https://github.com/OksanichenkoFedor/MultigrammTokenizer',
    packages=find_packages(include=["mg_tok"]),
    ext_modules=[module_cfuncs],
    author='Oksanichenko Fedor',
    author_email="okssolotheodor@gmail.com",
    description='Multigramm Tokenization package',
    long_description='A Python implementation of ngram-tokenization algorithm.',
    install_requires=[
        "numpy >= 1.21.5",
        "tqdm >= 4.64.0"
    ],
    license='MIT'
)