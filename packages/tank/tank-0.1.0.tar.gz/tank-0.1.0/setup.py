"""
tank is a tool to predict the rank of a tensor.
"""
from setuptools import setup

setup(
    name='tank',
    version='0.1.0',
    author='William Shiao',
    author_email='willshiao@gmail.com',
    packages=['tank'],
    scripts=[],
    url='http://pypi.python.org/pypi/tank/',
    license='LICENSE',
    description='A collection of useful functions/classes for data analysis and ML.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
