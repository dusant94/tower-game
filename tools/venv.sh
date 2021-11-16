#!/usr/bin/env bash

# this script will initialize python virtual environment, 
# if env exists it will just activate
# else it will create one and install all requirements, then will activate
#
# Note: To run thus, you must use 
#	". ./tools/venv.sh"


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR="$( dirname "${SCRIPT_DIR}" )"

export PYTHONPATH="$PROJECT_DIR"
ENV="${PROJECT_DIR}/.venv"

if [[ ! -d $ENV ]]
then
    echo 'Initializing environment ...'
    virtualenv $ENV
    source ${ENV}/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo 'Activating virtual environment ...'
    source ${ENV}/bin/activate
fi
