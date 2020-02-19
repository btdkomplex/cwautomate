import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CWAutomate",  # Replace with your own username
    version="0.0.1",
    author="Barry Collins",
    author_email="btdcollins@outlook.com",
    description="An interface for controlling Connectwise Automate (formerly Labtech)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/btdkomplex/cwautomate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
