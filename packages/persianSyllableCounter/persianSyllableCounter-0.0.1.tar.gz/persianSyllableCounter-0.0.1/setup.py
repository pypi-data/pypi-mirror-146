import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="persianSyllableCounter",
    version="0.0.1",
    author="Sina Salimian",
    author_email="sina99.sn@gmail.com",
    description="A package used for counting syllables in persian texts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salsina/Persian-syllable-counter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)