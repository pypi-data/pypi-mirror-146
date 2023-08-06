from setuptools import setup
from pathlib import Path


CURRENT_DIR = Path(__file__).parent

long_description = (CURRENT_DIR / "README.md").read_text(encoding="utf8")

description = "sarscov2vec is an application of continuous vector space representation on novel species" \
              " of coronaviruses genomes as the methodology of genome feature extraction step, to distinguish" \
              " the most common different SARS-CoV-2 variants by supervised machine learning model."

# Read requirements and process as list of strings
dependencies = (CURRENT_DIR / "requirements.txt").read_text()
dependencies = list(map(str.strip, filter(None, dependencies.split("\n"))))


version = "1.0.0"

setup(
    name="sarscov2vec",
    version=version,
    license="MIT",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Piotr Tynecki & Marcin Lubocki",
    author_email="p.tynecki@doktoranci.pb.edu.pl",
    url="https://github.com/ptynecki/sarscov2vec",
    download_url=f"https://github.com/ptynecki/sarscov2vec/archive/v{version}.tar.gz",
    setup_requires=["setuptools>=50.3.0", "wheel>=0.35.1"],
    install_requires=dependencies,
    packages=[
        "tools"
    ],
    data_files=[],
    include_package_data=True,
    keywords=[
        "SARS-CoV-2",
        "GISAID",
        "COVID-19",
        "continuous embedding",
        "genome sequence embedding",
        "virus bioinformatics",
        "sequence analysis"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
)
