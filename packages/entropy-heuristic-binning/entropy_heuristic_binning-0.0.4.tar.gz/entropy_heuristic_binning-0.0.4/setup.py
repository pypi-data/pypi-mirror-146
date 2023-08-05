from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="entropy_heuristic_binning",
    version="0.0.4",
    author="shazri_shahrir",
    author_email="mdshazrishahrir@gmail.com",
    description="entropy heuristic binning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shazri/entropyheuristicbinning",
    packages=setuptools.find_packages(),
    python_requires='>=3.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_save=False
)