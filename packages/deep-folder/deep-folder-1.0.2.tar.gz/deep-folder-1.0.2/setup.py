import setuptools

from deepfolder import remove

remove("./build")
remove("./dist")
remove("./deep_folder.egg-info")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deep-folder",
    version="1.0.2",
    author="sotaneum",
    author_email="gnyontu39@gmail.com",
    description="create or remove a simple folder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sotaneum/deep-folder",
    packages=setuptools.find_packages(exclude=['exmple']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
