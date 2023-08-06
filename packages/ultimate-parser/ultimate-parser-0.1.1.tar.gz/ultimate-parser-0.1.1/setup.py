from setuptools import setup, find_packages

VERSION = "0.1.1"
DESCRIPTION = "A simple parser."

setup(
    name="ultimate-parser",
    version=VERSION,
    author="Swanchick (Kyryl Lebedenko)",
    author_email="Kiryll.Swan@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests']
)