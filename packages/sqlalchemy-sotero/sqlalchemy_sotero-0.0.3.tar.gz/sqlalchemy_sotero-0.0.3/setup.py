import os
from setuptools import setup, find_packages

setup(
    include_package_data=True,
    install_requires=["SQLAlchemy", "JayDeBeApi"],
    zip_safe=False,
    keywords="Sotero SQLAlchemy JDBC Dialect",
)
