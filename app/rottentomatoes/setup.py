from setuptools import setup, find_packages


VERSION = "0.3.2"
DESCRIPTION = (
    "Scrape Rotten Tomatoes's website for basic information on movies, without the " \
        "use of their hard-to-attain official REST API."
)


def read_me():
    with open("README.md", "r") as f:
        return f.read()


# Set it up
setup(
    name="rottentomatoes-python",
    version=VERSION,
    author="Prerit Das",
    author_email="<preritdas@gmail.com>",
    description=DESCRIPTION,
    long_description=read_me(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires = ["requests"],
    keywords=["python", "movies", "rottentomatoes"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
