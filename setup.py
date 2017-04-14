from setuptools import setup

__version__ = "1.0.1"

setup(
        name="metabase",
        version=__version__,
        description='python wrapper for metabase api',
        url="https://github.com/stunitas/metabase-py",
        license="MIT License",
        author="flrngel",
        author_email="flrngel@gmail.com",
        install_requires=["requests==2.13.0"] )
