from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package_image_processing",
    version="0.0.1",
    author="Irene Santos",
    author_email="ireneptc87@gmail.com",
    description="Criação de pacotes de processamento de imagens",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IreneSantos872/pacoteprocessamentoimagens",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)