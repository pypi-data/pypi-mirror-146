import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = []
    for package in f.readlines():
        requirements.append(package.strip())

setuptools.setup(
    name="feather_creator",
    version="0.0.2",
    author="Timothée Frouté and Sergio Peignier",
    author_email="sergio.peignier@insa-lyon.fr",
    description="motif-TG .feather files creation and motifs-TF mapping from a list",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires = requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)

print(setuptools.find_packages())
