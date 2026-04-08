FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

COPY lease_manager_web/ ./lease_manager_web/

EXPOSE 5000

CMD ["uv", "run", "flask", "--app", "lease_manager_web.app", "run", "--host", "0.0.0.0", "--port", "5000"]
