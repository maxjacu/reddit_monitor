from setuptools import find_packages
from setuptools import setup

setup(
    name='reddit_monitor',
    version='0.1',
    author='Max Jacubowsky',
    packages=find_packages(),
    install_requires=[
        'absl-py',
        'praw',
        'retry',
        'prawcore'
    ]
)
