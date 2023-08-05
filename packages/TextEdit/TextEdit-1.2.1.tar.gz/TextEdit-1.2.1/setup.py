import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TextEdit",
    version="1.2.1",
    author="Corentin Perdry",
    author_email="corentin.perdry@gmail.com",
    description="A small module for to display the letters at the sequence.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/C0rent1Perdry/TextEdit-1.0",
    project_urls={
        "Bug Tracker": "https://github.com/C0rent1Perdry/TextEdit-1.0/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['sound/*.wav']},
    python_requires=">=3.6",
)