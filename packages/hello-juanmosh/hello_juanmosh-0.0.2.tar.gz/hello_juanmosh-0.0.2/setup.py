from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="hello_juanmosh",
    version="0.0.2",
    author="juan",
    author_email="apolinario.psi@gmail.com",
    description="Simple Hello World",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juanapolinario/calc_package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)