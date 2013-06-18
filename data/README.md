OHHS Falcon - Data
==================

OHHS sample data is not found here, but can be imported and transformed into
a static directory of geographic data files.

Install
-------

Python packages are listed in `requirements.txt`, and can be downloaded and
actived in a [virtual environment](https://pypi.python.org/pypi/virtualenv)
like this:

    make
    source venv-ohhs-map/bin/activate

Usage
-----

`python import.py` will import OHHS data from a remote URL and index it into
a directory of [GeoJSON](http://www.geojson.org/) files in `tiles`.
