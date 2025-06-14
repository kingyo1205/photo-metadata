from setuptools import setup, find_packages
import os

setup(
    name="photo_metadata",
    version="0.1.3",
    packages=find_packages(),
    description="Python library for accessing photo and video metadata via exiftool",
    long_description=open(
        os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kingyo1205/photo-metadata",
    author="ひろ",
    author_email="hirokingyo.sub@gmail.com",

    install_requires=[
        "tqdm"
    ],

    python_requires=">=3.10",

    package_data={
        "photo_metadata": [
            "exiftool_Japanese_tag.json",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)