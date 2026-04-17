FROM python:3.12-slim AS base

LABEL maintainer="Niyam-Projects Contributors"
LABEL description="Niyam Agent Starters — local development runner"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uv

# ---- Application ----
FROM base AS app
COPY . .
RUN uv pip install --system -e .

RUN useradd --create-home appuser
USER appuser

ENTRYPOINT ["niyam"]
CMD ["--help"]
