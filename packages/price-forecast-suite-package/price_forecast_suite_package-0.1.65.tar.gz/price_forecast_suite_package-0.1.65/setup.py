#!/usr/bin/env python
# coding=utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="price_forecast_suite_package",
    version="0.1.65",
    author="ZhangLe",
    author_email="zhangle@example.com",
    description="suite_data processing & modeling function",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://doc.com",
    project_urls={
        "Bug Tracker": "https://doc.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages("."),
    install_requires = [
      'pandas>=0.25.1',
      'numpy>=1.21.5', 
      'DateTime>=4.4', 
      'tensorflow>=2.2.0',
      'xgboost>=1.2.0',
      'scikit-learn>=1.0',
      'keras-tcn>=3.4.0',
      'matplotlib>=3.1.1',
      'pickleshare>=0.7.5',
      'cloudpickle>=1.2.2',
      'optuna>=2.10.0',
      'SQLAlchemy>=1.3.9'],
    python_requires=">=3.6",
)
