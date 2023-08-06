from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Linear Algebra Calculator with simple functions'
#LONG_DESCRIPTION = 'A linear algebra function that uses python to calculate values such as the inverse or transpose of a matrix and much more'

# Setting up
setup(
    name="linearAlgebraVectorMath",
    version=VERSION,
    author="Aditya Srikanth",
    author_email="aditya.srikanth11@gmail.com" ,
    description=DESCRIPTION,
    #long_description_content_type="text/markdown",
    #long_description=long_description,
    packages=find_packages(),
    install_requires=['traceback'],
    keywords=['python', 'mathamatics', 'Linear Algebra', 'Vectors', 'Eigen Values'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)