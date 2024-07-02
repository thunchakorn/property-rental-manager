FROM python:3.12.4-bullseye as builder

ARG DEV=false

RUN pip install poetry==1.8.3

# set environment variables
ENV POETRY_NO_INTERACTION=1 \ 
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \ 
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev,test --no-root

RUN if [ $DEV ]; then \
      poetry install --with dev,test --no-root && rm -rf $POETRY_CACHE_DIR; \
    else \
      poetry install --without dev,test --no-root && rm -rf $POETRY_CACHE_DIR; \
    fi

FROM python:3.12.4-slim-bullseye as runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app .
COPY . .

# install psycopg2 dependencies
# RUN apt-get update && apt-get install -y postgresql

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]