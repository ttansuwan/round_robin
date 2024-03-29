FROM python:3.11

ARG INSTALL_ENV

WORKDIR /app/

ENV INSTALL_ENV=${INSTALL_ENV} \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY ../poetry.lock ../pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN bash -c "if [ $INSTALL_ENV != 'production' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

COPY ./instance/app /app
ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
