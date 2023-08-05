from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="texto_no_espelho",
    version="0.0.1",
    author="Israel Ruiz",
    author_email="israelruiz2005@gmail.com",
    description="Texto no espelho",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/israelruiz2005/texto_no_espelho_package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)