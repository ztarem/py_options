import setuptools

with open("my_options_parser/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_options_parser",
    version="0.2",
    author="Zvi Tarem",
    author_email="zvi.tarem@gmail.com",
    description="Enhanced commandline options parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
