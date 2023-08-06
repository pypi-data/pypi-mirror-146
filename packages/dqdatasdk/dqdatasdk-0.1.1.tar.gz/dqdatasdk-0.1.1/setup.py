# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import versioneer

setup(
    name="dqdatasdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="DigQuant Data SDK",
    long_description_content_type='text/markdown',
    download_url="https://pypi.org/",
    include_package_data=True,
    packages=find_packages(include=["dqdatasdk"]),
    install_requires=["rqdatac"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    zip_safe=False,
    package_data={"": ["*.*"]},
)
