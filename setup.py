import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flab",
    version="2.0.3",
    author="Nicholas A. Jose",
    author_email="njose40707@gmail.com",
    description='A fast, flexible and fun framework for creating automated laboratories',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/njoseGIT/flab",
    license='GNU GPL3',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)