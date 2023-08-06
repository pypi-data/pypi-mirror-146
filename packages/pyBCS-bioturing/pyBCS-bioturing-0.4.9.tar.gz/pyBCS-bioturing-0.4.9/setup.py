import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = {}
with open("pyBCS/version.py", "r") as f:
    exec(f.read(), version)

setuptools.setup(
    name="pyBCS-bioturing",
    version=version["__version__"],
    author="BioTuring",
    author_email="support@bioturing.com",
    description="Create BioTuring Compressed Study (bcs) file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.bioturing.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "scanpy>=1.6.0",
        "anndata>=0.7.5",
        "loompy>=3.0.6",
        "xmltodict>=0.12.0",
        "imagecodecs>=2022.2.22",
        "openpyxl>=3.0.9",
        "xlrd>=1.0.0",
        "opencv-python>=4.5.5",
        "tifffile",
    ],
)
