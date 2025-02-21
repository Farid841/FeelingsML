FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config netcat-traditional && \
    apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure models directory exists
COPY models/ models/

COPY . .

ENV FLASK_APP=app
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]