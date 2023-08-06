from setuptools import find_packages, setup
import os

def get_readme():
    file = os.path.join(os.path.dirname(__file__), "README.md")
    with open(file) as f:
        return f.read().strip()

setup(
    name="ltbfiles",
    author="Sven Merk",
    description="Module for loading of files created with spectrometers from LTB",
    long_description=get_readme(),
    packages=find_packages(),
    include_package_data=True,
    url="https://gitlab.com/ltb_berlin/ltb_files",
    install_requires=['numpy'],
    extras_require={
        'tests': ['pytest'],
        'publish': ['twine','wheel'],
    }
)