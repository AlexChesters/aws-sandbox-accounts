set -e

export PATH="${HOME}/.poetry/bin:${PATH}"

poetry install --without dev

export VENV_PATH=$(poetry env info -p)

mkdir build
cp -R ${VENV_PATH}/lib/python3.*/site-packages/* build/
cp -R db_client build/
