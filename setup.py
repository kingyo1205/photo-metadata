from setuptools import setup, find_packages
import os
import sys

if not (sys.platform.startswith("linux") or sys.platform.startswith("win32")):
    raise RuntimeError(
        "This library only supports Linux and Windows. Other operating systems are not supported."
    )

setup(
    name="photo-metadata",
    version="0.3.2",
    packages=find_packages(),
    description="Python library to extract, read, modify, and write photo and video metadata (EXIF, IPTC, XMP) using ExifTool. Supports JPEG, RAW, and video files.",
    keywords="photo, image, metadata, exif, exiftool, iptc, xmp, video, camera, photography, raw, jpeg, picture, python, library, read, write, edit",
    long_description=open(
        os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kingyo1205/photo-metadata",
    author="kingyo1205",
    author_email="kingyo.programming@gmail.com",
    install_requires=[
        "tqdm",
        "charset-normalizer"
    ],
    license="MIT",
    license_files=["LICENSE"], 
    python_requires=">=3.11",
    package_data={
        "photo_metadata": [
            "exiftool_japanese_tag.json",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia :: Graphics :: Capture",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://github.com/kingyo1205/photo-metadata#readme",
        "Source": "https://github.com/kingyo1205/photo-metadata",
        "Tracker": "https://github.com/kingyo1205/photo-metadata/issues",
    },
)
