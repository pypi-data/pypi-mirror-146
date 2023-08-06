from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NephLib",
    version="0.0.1",
    author="Brandon Pooler",
    author_email="brandon.pooler@ibm.com",
    description="A collection of frequently used functions & modules. For quick importing.",
    long_description=long_description,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
)
