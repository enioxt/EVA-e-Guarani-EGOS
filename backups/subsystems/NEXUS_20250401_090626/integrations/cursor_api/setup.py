"""
Setup script for cursor-api package.
"""

from setuptools import setup, find_packages

setup(
    name="cursor-api",
    version="1.0.0",
    description="EVA & GUARANI - Cursor IDE Integration API",
    author="EVA & GUARANI",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
