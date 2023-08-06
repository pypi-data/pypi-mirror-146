import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="soco_trainer_plugin",
    packages = find_packages(),
    include_package_data=True,
    version="0.1.13",
    author="kyusonglee",
    description="Plugin helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.soco.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'pymongo[srv] == 3.7.2',
        'requests >= 2.23.0',
        "redis==3.3.11",
        "rq==1.1.0",
        "docker==4.4.0",
        "kubernetes==12.0.1",
        "flask",
        "flask_cors",
        "numpy==1.21.2",
        "pytorch_lightning",
        "glob2"
    ]
)