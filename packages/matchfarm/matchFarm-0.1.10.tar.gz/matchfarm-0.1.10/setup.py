from setuptools import setup, find_packages
import os.path

curdir = os.path.dirname(__file__)

readmePath = os.path.join(curdir, "README.md")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'matchfarm',
    version = '0.1.10',
    author = 'Carson Vache',
    author_email = 'carsonvache@gmail.com',
    license = 'GNU GENERAL PUBLIC LICENSE',
    description = 'Farm LOL matches',
    long_description = open(readmePath).read(),
    long_description_content_type = "text/markdown",
    url = 'https://github.com/cvache/LeagueMatchFarm',
    #py_modules = ['matchFarm', 'src'],
    packages = find_packages("src"),
    package_dir = {"": "src",},
    install_requires = [
        "requests",
        "riotwatcher",
        "boto3",
        ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ]
)