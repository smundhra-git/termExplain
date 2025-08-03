#!/usr/bin/env python3
"""
Setup script for termExplain
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    here = os.path.abspath(os.path.dirname(__file__))
    req_path = os.path.join(here, "requirements.txt")
    with open(req_path, "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]


setup(
    name="termexplain",
    version="1.0.1",
    author="Shlok Mundhra",
    author_email="shlokmundhra1111@gmail.com",
    description="AI-powered CLI error explainer using Gemini",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/smundhra-git/termExplain",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    packages=find_packages(include=["termexplain", "termexplain.*"]),
    entry_points={
    "console_scripts": [
        "termexplain=termexplain.cli:main",
        "explain=termexplain.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.sh"],
    },
    keywords="cli, error, explanation, ai, gemini, terminal, debugging",
    project_urls={
        "Bug Reports": "https://github.com/smundhra-git/termExplain/issues",
        "Source": "https://github.com/smundhra-git/termExplain",
        "Documentation": "https://github.com/smundhra-git/termExplain#readme",
    },
)