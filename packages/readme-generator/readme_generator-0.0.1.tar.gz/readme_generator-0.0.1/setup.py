import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="readme_generator",
    version="0.0.1",
    author="Piotr Ostrowski",
    author_email="piotr.ostrowski@aol.com",
    description="Very simple readme generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/piotrostr/readme_generator",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
