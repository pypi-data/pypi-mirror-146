from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'prints a funny line to the console'
LONG_DESCRIPTION = 'a python package which prints a line related to farts to the console an amount of times desired by the user'

setup(
        name="pyFart", 
        version=VERSION,
        author="Brendan Corcoran",
        author_email="brendan.j.corcoran@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python', 'fart'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
