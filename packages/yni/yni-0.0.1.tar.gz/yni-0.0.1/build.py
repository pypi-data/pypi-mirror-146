with open("requirements.txt", "r") as f:
    requirements = f.readlines()


def build(setup_kwargs: dict):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update({"install_requires": requirements})
