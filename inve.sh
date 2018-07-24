#! /bin/sh

export VIRTUAL_ENV="./venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME
exec "${@:-$SHELL}"
