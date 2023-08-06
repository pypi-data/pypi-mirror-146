from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="stringoperations_subhra",
    version="1.0.1",
    description="Program to perform operations on string",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Subhra Subudhi ",
    author_email="subhra.subudhi@yahoo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["string_ops_subhra"],
    include_package_data=True,
)