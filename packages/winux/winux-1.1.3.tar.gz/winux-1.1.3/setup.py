from setuptools import setup
from pathlib import Path

directory = Path(__file__).parent
longDescription = (directory/'README.md').read_text()

setup(
    name='winux',
    author='Cargo',
    version='1.1.3',
    long_description=longDescription,
    long_description_content_type='text/markdown',
    packages=['winux'],
    install_requires=['click'],
    entry_points=
    '''[console_scripts]
    clear=winux:clear
    ls=winux:ls
    mv=winux:mv
    cp=winux:cp
    rm=winux:rm
    cat=winux:cat
    pwd=winux:pwd
    date=winux:date
    nano=winux:nano
    mem=winux:mem
    kill=winux:kill
    man=winux:man
    mkdir=winux:mkdir
    ps=winux:psX
    '''
)
