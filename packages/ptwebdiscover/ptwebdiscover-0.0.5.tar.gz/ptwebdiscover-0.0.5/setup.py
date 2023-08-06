import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptwebdiscover",
    version="0.0.5",
    description="Web Source Discovery Tool",
    author="Penterep",
    author_email="info@penterep.com",
    url="https://www.penterep.com/",
    license="GPLv3+",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console"
    ],
    python_requires='>=3.6',
    install_requires=["ptlibs>=0.0.6", "ptthreads", "requests", "treelib", "tldextract", "idna", "appdirs", "filelock"],
    entry_points = {'console_scripts': ['ptwebdiscover = ptwebdiscover.ptwebdiscover:main']},
    long_description=long_description,
    long_description_content_type="text/markdown",
)
