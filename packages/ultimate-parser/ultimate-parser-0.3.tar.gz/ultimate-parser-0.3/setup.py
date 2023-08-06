from setuptools import setup, find_packages

VERSION = "0.3"
DESCRIPTION = "A simple parser."

setup(
    name="ultimate-parser",
    version=VERSION,
    author="Swanchick (Kyryl Lebedenko)",
    url='https://github.com/Swanchick/ultimate-parser',
    author_email="Kiryll.Swan@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests']
)