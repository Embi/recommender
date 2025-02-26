FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY pipelines /app/pipelines
COPY core /app/core

WORKDIR /app

RUN pip install --no-cache-dir --upgrade \
  -r ./pipelines/requirements.txt \
  -r ./core/requirements.txt

CMD ["bash", "pipelines/run_pipeline.sh"]
