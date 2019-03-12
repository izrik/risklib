#!/bin/bash

SOURCES=riskcli

#coverage run --source=$SOURCES --branch -m unittest discover -s tests -p '*.py' -t . "$@" && \
#    coverage html

python -m unittest discover -s tests -p '*.py' -t . "$@"
