from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

#with open("requirements.txt") as f:
#    requirements = f.read().splitlines()

setup(
    name="calculadora-package-jcnok",
    version="0.0.1",
    author="Julio Okuda",
    author_email="julio.okuda@gmail.com",
    description="Meu primeiro pacote",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jcnok/myfirst_package.git",
    packages=find_packages(),
    install_requires=[],#requirements,
    python_requires='>=3.8.10',
)