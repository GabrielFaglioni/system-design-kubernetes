# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim-bullseye

RUN apt-get update \
  && apt-get install -y --no-install-recommends  --no-install-suggests \
  build-essential \
  pkg-config \
  default-libmysqlclient-dev \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt -v
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]