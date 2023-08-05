import setuptools

with open("README.md", "r") as file:

    long_description = file.read()

setuptools.setup(
    name="pyb3",
    version="0.0.1",
    author="Victor Martins",
    author_email="victor.martins.dpaula@gmail.com",
    description="B3 (b3.com.br) API wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/victormpa/pyb3",
    project_urls={
        "Bug Tracker": "https://github.com/victormpa/pyb3/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9"
)
