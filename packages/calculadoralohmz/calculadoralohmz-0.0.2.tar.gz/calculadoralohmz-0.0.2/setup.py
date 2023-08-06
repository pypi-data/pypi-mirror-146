from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="calculadoralohmz",
    version="0.0.2",
    author="simon",
    author_email="simonssilva08@gmail.com",
    description="Calculadora bem básica",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simonssilva/projeto-dio-calculadoralohmz",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8'
)