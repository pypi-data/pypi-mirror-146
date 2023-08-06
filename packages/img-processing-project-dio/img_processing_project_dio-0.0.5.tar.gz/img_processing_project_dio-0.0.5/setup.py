from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="img_processing_project_dio",
    version="0.0.5",
    author="Thielson Alemendra",
    author_email="thielson12@gmail.com",
    description="This project is part of a bootcamp",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BetaTH/image_processing_th.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)