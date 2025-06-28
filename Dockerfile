# Use official Python runtime as base image
FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install basic dependencies only
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p reports
RUN chmod +x run_tests.sh
CMD ["./run_tests.sh"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://jsonplaceholder.typicode.com/users || exit 1

LABEL maintainer="SDET Assignment"
LABEL version="1.0"
LABEL description="FanCode SDET Assignment Test Suite"
