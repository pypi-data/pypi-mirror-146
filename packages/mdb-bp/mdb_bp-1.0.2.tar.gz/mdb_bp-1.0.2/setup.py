from setuptools import setup, find_packages


VERSION = '1.0.2'
DESCRIPTION = 'blockpoint Systems - MultiVersion Database (MDB) ODBC'
LONG_DESCRIPTION = open("README.md").read() # 'This package provides ... ... ... '

# Setting up
setup(
    name="mdb_bp",
    version=VERSION,
    author="Blockpoint Systems",
    author_email="<info@blockpointdb.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'grpcio', 'grpcio-tools', "google"
    ],
    tests_require=['pytest'],
    url='https://gitlab.com/blockpoint/mdb-odbc-python',

    keywords=['blockpoint', 'mdb_bp', 'odbc', 'blockchain', 'database'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Database",
        # "Topic :: ODBC",
        # "Topic :: Blockchain",
        # "Topic :: Blockchain Database",
        # "Topic :: MultiVersion Database",
    ]
)
