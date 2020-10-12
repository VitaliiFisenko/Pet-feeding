FROM python:3.8-slim as base
WORKDIR /backend/src
ENV PYTHONUNBUFFERED True
COPY /backend/requirements.txt .
RUN pip install -r requirements.txt


FROM base as prod
COPY backend/src .

FROM prod