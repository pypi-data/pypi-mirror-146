#!/usr/bin/env python
import sys
version = sys.argv[1]
del sys.argv[1]
from setuptools import setup, find_packages

setup(
    name='test-uqpy',
    version=version,
    license='MIT',
    platforms=["OSX", "Windows", "Linux"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["*.pdf"]},
    install_requires=[
        "numpy", "scipy", "matplotlib", "scikit-learn", 'fire',
        "beartype==0.9.1",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)
