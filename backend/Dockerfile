FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev build-essential netcat-traditional

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONUNBUFFERED=1
# dos2unix backend/waitdb.sh [TODO]
COPY waitdb.sh .
RUN chmod +x waitdb.sh