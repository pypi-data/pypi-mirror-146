from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'MatchFarm',
    version = '0.1.4',
    author = 'Carson Vache',
    author_email = 'carsonvache@gmail.com',
    license = 'GNU GENERAL PUBLIC LICENSE',
    description = 'Farm LOL matches',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/cvache/LeagueMatchFarm',
    py_modules = ['matchFarm', 'src'],
    packages = find_packages(),
    install_requires = [
        "requests",
        "riotwatcher",
        "boto3",
        "json"     
        ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ]
)