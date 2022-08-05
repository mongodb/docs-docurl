from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="docurl",
    version="0.2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mongodb/docs-docurl",
    py_modules=["src"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["Click", "tomli", "tomli_w", "PyGithub", "py-console"],
    entry_points={
        "console_scripts": [
            "docurl = src.main:docurl",
        ],
    },
)
