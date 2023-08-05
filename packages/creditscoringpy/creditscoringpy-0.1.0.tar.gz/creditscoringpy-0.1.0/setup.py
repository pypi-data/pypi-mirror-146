from setuptools import setup, find_packages


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=1.4.2"]

setup(
    name="creditscoringpy",
    version="0.1.0",
    author="Alexey Myshlyanov",
    author_email="avmysh@gmail.com",
    description="A package for building scorecards in python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/creditscoringpy/creditscoringpy",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
    ],
)