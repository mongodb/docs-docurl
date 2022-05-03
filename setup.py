from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="docurl",
    version="0.1.5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/terakilobyte/docurl",
    py_modules=["src"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "docurl = src.main:docurl",
        ],
    },
)
