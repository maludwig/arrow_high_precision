#!/bin/bash

function printandrun {
  echo "------ $@ ------"
  "$@"
  echo "--------------------------"
}
#
#printandrun pwd
#printandrun which brew
#printandrun which pyenv
#printandrun which python
#printandrun which python2
#printandrun which python3
#
#printandrun pyenv versions
#printandrun pyenv install --list
#printandrun brew ls
#printandrun set
#printandrun pip install -r requirements.txt
#printandrun echo "$TOXENV"

# pyenv install --list | grep "$PYTHON_VERSION"

find_best_python_version () {
  PYTHON_VERSION="$1"
  ALL_SUBVERSIONS=`pyenv install --list | grep -E "^ +$PYTHON_VERSION.*?$" | tr -d ' '` 
  ALL_NUMBERED=`echo "$ALL_SUBVERSIONS" | grep -E "$PYTHON_VERSION"'\.[0-9]+$'`
  if [[ -z $ALL_NUMBERED ]]; then
    ALL_DEV=`echo "$ALL_SUBVERSIONS" | grep '\-dev'`
    if [[ -z $ALL_DEV ]]; then
      echo "No version found for $PYTHON_VERSION" 1>&2
      exit 1
    else
      echo "$ALL_DEV" | tail -n 1
    fi
  else
    echo "$ALL_NUMBERED" | tail -n 1
  fi
}

if PYENV_VERSION=`find_best_python_version "$PYTHON_VERSION"`; then
  pyenv install "$PYENV_VERSION"
  pyenv local "$PYENV_VERSION"
fi