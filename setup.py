from setuptools import setup
import setuptools

setup(
    name="tenzing",
    version="0.1.0",
    py_modules=["src"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "tenzing = src.main:tenzing",
        ],
    },
)
