ARG APP_IMAGE=python

FROM $APP_IMAGE AS base

RUN mkdir /project
WORKDIR /project
ADD . /project

RUN pip install -r requirements.txt

ENV FLASK_APP app.py
ENV FLASK_ENV development

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
