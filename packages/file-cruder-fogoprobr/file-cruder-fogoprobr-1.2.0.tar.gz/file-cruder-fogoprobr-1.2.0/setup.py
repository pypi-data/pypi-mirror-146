import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

REPOSITORY_URL = 'https://github.com/melattofogo/file-cruder-fogoprobr'

AUTHOR_NAME = 'Joao Fogo'

AUTHOR_EMAIL ='melatto.fogo@live.com'

setup(
    name="file-cruder-fogoprobr",
    version="1.2.0",
    packages=find_packages(exclude=('test', 'config')),
    include_package_data=True,
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    url=REPOSITORY_URL,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
)