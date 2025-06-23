#!/usr/bin/env python3
"""
AMIF Grant Assistant - Setup Paketi
"""

from setuptools import setup, find_packages
import os

def read_requirements():
    """Requirements.txt dosyasını okur"""
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def read_readme():
    """README.md dosyasını okur"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "AMIF Grant Assistant - AI-Powered Grant Document Q&A System"

setup(
    name="amif-grant-assistant",
    version="1.0.0",
    description="AI-Powered Grant Document Q&A System for AMIF grants",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Grant Spider Team",
    author_email="info@grantspider.com",
    url="https://github.com/FethiOmur/GrantSpider_Chatbot",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'amif-assistant=main:main',
            'amif-start=start:main',
            'amif-streamlit=streamlit_app:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Office/Business",
    ],
    keywords="ai nlp chatbot grants amif document-qa langchain vector-database",
    project_urls={
        "Bug Reports": "https://github.com/FethiOmur/GrantSpider_Chatbot/issues",
        "Source": "https://github.com/FethiOmur/GrantSpider_Chatbot",
        "Documentation": "https://github.com/FethiOmur/GrantSpider_Chatbot/blob/main/README.md",
    },
    include_package_data=True,
    zip_safe=False,
) 