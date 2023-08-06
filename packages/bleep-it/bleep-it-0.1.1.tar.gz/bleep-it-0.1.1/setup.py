import setuptools

with open("README.md", 'r', encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="bleep-it",
    version="0.1.1",
    author="Marseel Eeso",
    author_email="marseeleeso@gmail.com",
    description="Text filtering tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marseel-E/bleep-it",
    project_urls={
        "Bug Tracker": "https://github.com/Marseel-E/bleep-it/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "bleep"},
    packages=setuptools.find_packages(where="bleep"),
    python_requires=">=3.9",
)
