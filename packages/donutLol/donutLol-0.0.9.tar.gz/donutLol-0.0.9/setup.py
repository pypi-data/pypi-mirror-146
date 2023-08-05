from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))


with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.9'
DESCRIPTION = 'Prints a 3d donut'

# Setting up
setup(
    name="donutLol",
    version=VERSION,
    scripts=['donut.bat'] ,
    author="lazylion2",
    author_email="<lazylion2@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    url="https://github.com/lazylion22/donutLol",
    keywords=['python', 'donut', 'donut3d'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
