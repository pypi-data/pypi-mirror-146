from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


NAME = "bn2vec"
VERSION = "1.0.0"

setup(
    name=NAME,
    version=VERSION,
    description='Boolean Network To Vector',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mohamed Hmini',
    author_email='mo@mhmini.com',
    url='',
    packages=find_packages(include=['bn2vec', 'bn2vec.*']),
    install_requires=[
        'colomoto-jupyter==0.8.2',
        'igraph==0.9.9',
        'matplotlib==3.5.1',
        'numpy==1.22.2',
        'pandas==1.4.1',
        'scikit-learn==1.0.2',
        'tqdm==4.63.0',
        'PyYAML'
    ]
)
