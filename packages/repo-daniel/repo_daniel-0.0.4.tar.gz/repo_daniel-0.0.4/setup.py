# python setup.py bdist_wheel 
# to build the wheel
# to pip install this from the repo_daniel folder run
# pip install -e .
# to use run from hello_world import say_hello
# you can then use the function say_hello()
from setuptools import setup


with open("README.md", "r") as fh:
    long_description=fh.read()

setup(
    name='repo_daniel',
    version='0.0.4',
    description = 'junk',
    py_modules="[hello_world]",
    package_dir ={'': 'src'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['textfsm>=1.1.2',],
    extras_require={
        "dev": ['pytest>=3.7']
    },
    url='https://github.com/GoreNetwork/test_package',
    author="Daniel Himes",
    author_email="dhimes@gmail.com",
)
