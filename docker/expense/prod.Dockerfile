FROM python:3.10.6-slim-buster as python-build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev

COPY pyproject.toml ./

WORKDIR /app/
RUN pip install poetry && poetry export --without dev --output requirements.txt
RUN pip wheel --wheel-dir /usr/src/app/wheels  -r requirements.txt

FROM python:3.10.6-slim-buster as python-run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

RUN addgroup --system tracker \
    && adduser --system --ingroup tracker tracker

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./docker/expense/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/expense/start-prod.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --chown=tracker:tracker . /app/
RUN chown tracker:tracker /app/

USER tracker

ENTRYPOINT ["/entrypoint"]
