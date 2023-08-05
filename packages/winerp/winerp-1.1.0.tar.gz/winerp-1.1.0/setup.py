import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="winerp",
    version="1.1.0",
    description="Websocket based IPC for discord.py bots",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BlackThunder01001/winerp",
    project_urls={
        "Bug Tracker": "https://github.com/BlackThunder01001/winerp/issues",
    },
    author="BlackThunder",
    author_email="nouman0103@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        
    ],
    packages=["winerp"],
    package_data={
     'winerp.lib': ['*'],
    },
    include_package_data=True,
    install_requires=["websockets", "websocket-server"],
    python_requires=">=3.6",
)