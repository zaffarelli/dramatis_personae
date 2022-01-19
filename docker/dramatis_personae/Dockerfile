FROM centos/python-36-centos7:latest
USER root

RUN yum install -y httpd httpd-devel

ENV PATH="/scripts:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
ENV USER dp
ENV POETRY_VIRTUALENVS_CREATE=0
ENV WEB_PATH="/vol/web"

WORKDIR $WEB_PATH/app

COPY . .
COPY ./docker/dramatis_personae/custom.py ./dramatis_personae/settings/
COPY ./docker/dramatis_personae/dp.entrypoint.sh .


RUN pip install pip --upgrade
RUN pip install poetry
RUN poetry install --no-interaction

RUN mkdir -p /var/log/dramatis_personae && \
    touch /var/log/dramatis_personae/dramatis_personae.log

RUN mkdir -p $WEB_PATH/dp_media
RUN mkdir -p $WEB_PATH/dp_static

RUN groupadd --system -g 1000 $USER && \
    useradd --system -u 1000 -g 1000 --no-create-home $USER

RUN chown -R $USER: /vol
RUN chmod -R 755 /vol/web
RUN chown -R $USER: /var/log/dramatis_personae/

USER $USER

CMD ["./dp.entrypoint.sh"]



