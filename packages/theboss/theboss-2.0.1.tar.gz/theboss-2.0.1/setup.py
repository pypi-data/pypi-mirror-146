from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='theboss',
    version='2.0.1',
    author="Tomasz Rybotycki",
    author_email="rybotycki.tomasz+theboss@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    description="A package for (Bo)son (S)ampling (S)imulations!",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.7"',
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
    ],
    license="Apache License 2.0.",
)
