FROM python:3.8.5-alpine3.11 as base

FROM base as builder

WORKDIR /install

RUN apk update && apk add gcc ffmpeg postgresql-dev python3-dev musl-dev --no-cache

COPY requirements.txt /

RUN pip install --prefix=/install -r /requirements.txt

FROM base

RUN apk add libpq openssl ffmpeg --no-cache

COPY --from=builder /install /usr/local

WORKDIR /app

COPY bass_bot/ .

CMD ./launch.sh