from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ConversorBR",
    version="0.0.1",
    author="RNNSMP",
    author_email="renansampaio@id.uff.br",
    description="Converter mediadas usadas nos estados Unidos para medidas usadas no Brasil ",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RNNSNTS/ConversorBR",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)