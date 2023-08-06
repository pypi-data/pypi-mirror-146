from setuptools import setup, find_packages
import os

setup(
    name="geneseekr",
    version="0.5.0",
    packages=find_packages(),
    scripts=[
        os.path.join('geneseekr', 'GeneSeekr')
    ],
    author="Adam Koziol",
    author_email="adam.koziol@canada.ca",
    url="https://github.com/OLC-Bioinformatics/GeneSeekr",
)
