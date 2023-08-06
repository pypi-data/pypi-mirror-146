import setuptools
from pathlib import Path

directory = Path(__file__).parent
longDescription = (directory/'README.md').read_text()


setuptools.setup(
    name='kvk',
    version='1.1.5',
    author='Cargo',
    description='kvk file handler',
    long_description=longDescription,
    long_description_content_type='text/markdown',
    packages=['kvk']
)