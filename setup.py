import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='crime',
    version='0.1.4',
    description="Explore, load, and get documentation for Colorado crime data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/ryayoung/crime',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    author="Ryan Young",
    author_email='ryanyoung99@live.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='opendata socrata colorado crime',
    install_requires=[
          'pandas',
          'requests',
          'sodapy',
    ],
    python_requires='>=3.8'


)
