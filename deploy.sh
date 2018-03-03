!/bin/bash

pip install -U googlemaps

git clone https://github.com/googlemaps/google-maps-services-python.git

cd google-maps-services-python

pip install tox
tox

tox -e docs

easy_install wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*

tox -e docs && mv docs/_build/html genereated_docs && git clean -Xdi && git checkout gh-pages

