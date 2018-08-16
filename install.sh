#!/bin/bash

function printandrun {
    echo "------ $@ ------"
    "$@"
    echo "--------------------------"
}

printandrun pwd
printandrun which brew
printandrun which pyenv
printandrun which python
printandrun which python2
printandrun which python3

printandrun pyenv versions
printandrun pyenv install --list
printandrun brew ls
printandrun set
printandrun pip install -r requirements.txt
printandrun echo "$TOXENV"
