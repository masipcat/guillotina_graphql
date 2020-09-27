from setuptools import find_packages
from setuptools import setup


try:
    README = open("README.md").read()
except IOError:
    README = None

setup(
    name="guillotina_graphql",
    version="0.1.0",
    description="Provides a graphql endpoint to search the catalog",
    long_description=README,
    install_requires=["guillotina>=6.0", "ariadne~=0.12.0"],
    author="Jordi Masip",
    author_email="jordi@masip.cat",
    url="",
    packages=find_packages(exclude=["demo"]),
    include_package_data=True,
    tests_require=[
        "pytest",
    ],
    extras_require={"test": ["pytest"]},
    classifiers=[],
    entry_points={},
)
