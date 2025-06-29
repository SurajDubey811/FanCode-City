# Use official Python runtime as base image
FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gcc \
        dos2unix \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p reports
COPY run_tests.sh /app/run_tests.sh
RUN dos2unix /app/run_tests.sh \
    && chmod +x /app/run_tests.sh \
    && sed -i 's/\r$//' /app/run_tests.sh
ENV DOCKER_ENV=1
CMD ["/bin/bash", "/app/run_tests.sh"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://jsonplaceholder.typicode.com/users || exit 1

LABEL maintainer="SDET Assignment"
LABEL version="1.0"
LABEL description="FanCode SDET Assignment Test Suite"
