from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="calculadora_simples",
    version="0.0.1",
    author="Iago de Andrade",
    author_email="iago2005andrade@gmail.com",
    description="Calculadora com operadores simples",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iaguitchu/pacote_calculadora",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    setup_requires=['wheel']
)