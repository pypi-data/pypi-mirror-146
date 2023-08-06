from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="desafio_python_dio",
    version="0.0.1",
    author="Eric Cunha",
    author_email="ericscunha@hotmail.com",
    description="Pacote do Desafio de Projeto com base nos desafios de códigos do Bootcamp Cognizant Data Engineer 2",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericscunha/desafio-python-pkg-dio",
    packages=find_packages()
)