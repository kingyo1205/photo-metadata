from setuptools import setup, find_packages

setup(
    name="photo_metadata",
    version="0.1.0",
    packages=find_packages(),
    description="Photo Metadata library",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    install_requires=[
        "tqdm"
        
    ],

    package_data={
        'photo_metadata': [
            'exiftool_Japanese_tag.json',
        ],
    },

    classifiers=[
        "License :: OSI Approved :: MIT License",
        
    ],
)