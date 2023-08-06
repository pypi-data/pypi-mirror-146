"""The setup file"""
import re
import setuptools


VERSIONFILE = "cnvrg_extras/_version.py"
with open(VERSIONFILE, "rt", encoding="utf-8") as f:
    verstrline = f.read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError(f"Unable to find version string in {VERSIONFILE}.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cnvrg_extras",  # Replace with your own username
    version=verstr,
    author="Craig Smith",
    author_email="craig.smith@cnvrg.io",
    description="cnvrg helper SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nctiggy/cnvrg_extras",
    packages=setuptools.find_packages(),
    install_requires=[
        'cnvrgv2>=1.0.9',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
