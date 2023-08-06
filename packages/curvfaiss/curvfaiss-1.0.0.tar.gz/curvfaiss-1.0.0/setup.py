from __future__ import print_function
from setuptools import setup, find_packages
import os

long_description="""
Curvfaiss is a library for efficient similarity search and clustering of dense vectors in non-Euclidean manifolds.
The backbone is based on the Faiss project. Modifications are developed by Alibaba-Alimama Tech.
"""

setup(
    name='curvfaiss',
    version='1.0.0',
    description='A library for efficient similarity search and clustering of dense vectors in non-Euclidean manifolds',
    long_description=long_description,
    url='https://github.com/alibaba/Curvature-Learning-Framework',
    author='Zhirong Xu',
    author_email='zhirong.xzr@alibaba-inc.com',
    license='Apache',
    keywords='search nearest neighbors',

    install_requires=['curvlearn'],
    packages=['curvfaiss', 'curvfaiss.contrib'],
    include_package_data=True,
    package_data={
        'curvfaiss': ['*.so'],
    },
    zip_safe=False,
)

