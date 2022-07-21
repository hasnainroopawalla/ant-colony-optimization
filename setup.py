from setuptools import setup, find_packages
import os

repository_dir = os.path.dirname(__file__)

with open(os.path.join(repository_dir, "README.md")) as fh:
    long_description = fh.read()

setup(
    name="aco_routing",
    version="1.0.3",
    packages=find_packages(exclude="tests"),
    description="A Python package to find the shortest path in a graph using Ant Colony Optimization (ACO).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hasnainroopawalla/ant-colony-optimization",
    author="Hasnain Roopawalla",
    author_email="hasnain.roopawalla@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="python, machinelearning, ai, aco",
    python_requires=">=3.6",
)
