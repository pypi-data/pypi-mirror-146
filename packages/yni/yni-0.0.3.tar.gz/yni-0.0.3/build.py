import setuptools
import re

with open("requirements.txt", "r") as f:
    requirements = f.readlines()

with open("yni/__init__.py", "r") as f:
    read = f.read()
    version = re.search(r"__version__ = \"(.*?)\"", read).group(1)


def build(setup_kwargs: dict):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {
            "install_requires": requirements,
            "version": version,
            "packages": setuptools.find_packages(exclude=["tests"], include=["yni"]),
        }
    )
