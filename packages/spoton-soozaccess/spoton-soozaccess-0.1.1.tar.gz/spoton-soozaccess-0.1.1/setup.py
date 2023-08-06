import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="spoton-soozaccess",
    version="0.1.1",
    scripts=["bin/spoton-soozaccess"],
    author="Jean Demeusy",
    author_email="dev.jdu@gmail.com",
    description="A tool to access Spot-On API using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.forge.hefr.ch/pa-spot-on-demeusy/spot-on-soozaccess",
    packages=["spoton-soozaccess"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
