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
    version="0.0.6",
    description="fvisionNetwork14 is an image classification CNN model that can classify the  number of classes.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/KalyanMohanty/fvisionNetwork14",
    author="Kalyan Mohanty",
    author_email="kalyanrisingstar@gmail.com",
    keywords = ['fvisionNetwork14', 'fvNet14', 'image classification', 'deep neural network',
    'cnn', 'keras model', 'cnn'],
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