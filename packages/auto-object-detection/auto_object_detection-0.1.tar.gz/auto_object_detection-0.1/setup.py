
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open('required.txt') as f:
    required = f.read().splitlines()

setup(
    name="auto_object_detection",
    version="0.1",
    author="Elina Chertova",
    author_email="elas.2015@mail.ru",
    description="",
    python_requires='==3.7',
    long_description=readme,
    url="https://github.com/elina-chertova/tensorflow-2-object-detection.git",
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
)