FROM python:3.11-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.11-alpine

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY ./app ./app

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
