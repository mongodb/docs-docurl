from setuptools import setup
import setuptools

setup(
    name="docurl",
    version="0.1.3",
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
