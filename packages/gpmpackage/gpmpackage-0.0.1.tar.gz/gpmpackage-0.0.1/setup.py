from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "My first python package"
LONG_DESCRIPTION = "My first python package with a slightly longer description"

setup(
    name="gpmpackage",
    version=VERSION,
    author="Gerardo Perez",
    author_email="gerardopemz@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "gpm"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

