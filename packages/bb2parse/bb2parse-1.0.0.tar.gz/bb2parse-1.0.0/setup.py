from unicodedata import name
import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name= "bb2parse",
    version= "1.0.0",
    author= "Carsen Kennedy",
    author_email="carsenkennedy@pm.me",
    description= "Python wrapper for BloodBowl Match files",
    long_description=README,
    long_description_content_type ="text/markdown",
    url="https://github.com/CarsenKennedy/bb2parse",
    license ="MIT",
    install_requires =["ordered-set"],
    packages=setuptools.find_packages(include=['bb2parse','bb2parse.*'])
)