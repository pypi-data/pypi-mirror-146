import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Wind_is_not_decorator",
    version="0.20",
    author="liang233",
    author_email="Gavin_2009@163.com",
    description="Modify the functions dynamically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gavin4433/Wind",
    project_urls={
        "Bug Tracker": "https://github.com/Gavin4433/Wind/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)