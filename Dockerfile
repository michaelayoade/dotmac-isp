FROM python:3.12-slim AS builder

ARG POETRY_VERSION=2.4.1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1
WORKDIR /build

RUN apt-get update \
    && apt-get install --yes --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only main --no-root --sync

COPY src/dotmac_isp ./src/dotmac_isp
RUN poetry install --only main --sync

FROM python:3.12-slim AS runtime

ENV PATH=/app/.venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

RUN useradd --create-home --uid 10001 appuser
COPY --from=builder --chown=appuser:appuser /build/.venv /app/.venv

USER appuser
EXPOSE 8000
CMD ["uvicorn", "dotmac_isp.main:app", "--host", "0.0.0.0", "--port", "8000"]
