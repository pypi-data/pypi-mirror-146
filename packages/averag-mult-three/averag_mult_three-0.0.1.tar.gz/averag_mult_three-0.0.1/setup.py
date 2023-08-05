from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="averag_mult_three",
    version="0.0.1",
    author="Dimitri Marinho",
    author_email="dimitri.santana.marinho@gmail.com",
    description="Testando a criação de pacote em Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dimitrimarinho/averag_mult_three",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)