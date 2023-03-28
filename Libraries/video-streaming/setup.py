from setuptools import setup

VERSION = "0.1.1"

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="video-streaming",
    version=VERSION,
    author="MikiTwenty",
    author_email="terminetor.xx@gmail.com",
    description="Small package to simplify video streaming using python built-in socket library",
    packages=["videostreaming"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MikiTwenty/Python/tree/main/Libraries/socket-video-streaming",
    keywords=["python", "socket", "streaming", "server", "client"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["imutils"]
)