import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "snifflogic_air",
    version = "0.0.1",
    author = "snifflogic",
    author_email = "support@snifflogic.com",
    description = "Python SDK for communicating with the Sniff Controller Air of Sniff Logic",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/snifflogic/python-air",
    project_urls = {
        "Bug Tracker": "https://github.com/snifflogic/python-air/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "snifflogic_air"},
    packages = setuptools.find_packages(where="snifflogic_air"),
    python_requires = ">=3.6",
    requires=["bleak","rich"]
)