import pathlib
from setuptools import setup, find_packages

ROOT = pathlib.Path(__file__).parent
README = ROOT.joinpath("README.md").read_text()

setup(
    name="subtitle_normalizer",
    version="0.0.1",
    description="Some tools to reformat SubRipFiles",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Serbaf/subtitle_normalizer",
    author="Sergio Puche García",
    author_email="spuche@upv.es",
    license="GPL3",
    packages=find_packages()
)
