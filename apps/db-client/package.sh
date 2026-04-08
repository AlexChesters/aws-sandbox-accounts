set -e

uv sync --no-dev

mkdir build
cp -R .venv/lib/python3.*/site-packages/* build/
cp -R db_client build/
