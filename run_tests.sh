#!/bin/bash

SOURCES=riskcli
ALL_SOURCES="$SOURCES tools tests"

coverage run --source=$SOURCES --branch -m unittest discover -s tests -p '*.py' -t . "$@" && \
    coverage html && \
    flake8 $ALL_SOURCES
