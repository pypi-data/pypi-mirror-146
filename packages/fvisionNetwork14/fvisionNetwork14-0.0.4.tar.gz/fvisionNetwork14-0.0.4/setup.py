import pathlib
from setuptools import setup
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="fvisionNetwork14",
    version="0.0.4",
    description="fvisionNetwork14 is classification model, image preprocessing module will preprocess the image, plotting accuracy and loss grapghs plots the graphs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/KalyanMohanty/fvisionNetwork14",
    author="Kalyan Mohanty",
    author_email="kalyanrisingstar@gmail.com",
    license="MIT",
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
    ],
    # packages=["fvisionNetwork14"],
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
                    "matplotlib",
                    "numpy"
                    
    ]
)