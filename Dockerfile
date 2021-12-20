FROM python:3.6-alpine

ENV PATH="/scripts:${PATH}"
ENV PYTHONBUFFERED 1

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev libffi-dev linux-headers
RUN apk del .tmp

RUN mkdir /dramatis_personae
COPY ./dramatis_personae /dramatis_personae
WORKDIR /dramatis_personae
COPY ./scripts /scripts


ENV PIP_DISABLE_PIP_VERSION_CHECK=on
RUN pip install poetry
WORKDIR /dramatis_personae
COPY poetry.lock pyproject.toml /dramatis_personae/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
COPY . /dramatis_personae


RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]



