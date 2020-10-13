FROM python:3.8-slim as base
WORKDIR /src
ENV PYTHONUNBUFFERED True
COPY /requirements.txt .
RUN pip install -r requirements.txt


FROM base as prod
COPY /src .

FROM prod