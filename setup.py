import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="github-reporter",
    version="0.0.1",
    author="Barak Stout",
    author_email="???",
    description="script to extract github.com usage for user via github api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BarakStout/github-reporter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
