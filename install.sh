#!/bin/bash

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

if [[ -z $PYTHON_VERSION ]]; then
  echo "Skipping python install"
else
  if PYENV_VERSION=`find_best_python_version "$PYTHON_VERSION"`; then
    pyenv install "$PYENV_VERSION"
    pyenv local "$PYENV_VERSION"
  fi
fi
pip install -r requirements.txt
