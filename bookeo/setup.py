from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A Python implementation of the Bookeo API"
LONG_DESCRIPTION = (
    "A Python implementation of the Bookeo API, conversing in native types"
)

setup(
    name="bookeo",
    version=VERSION,
    author="Nolan Welch",
    author_email="nolanwelch@outlook.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests", "urllib3"],
    keywords=["python", "Bookeo"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    ],
)
