FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/src

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
COPY entrypoint.sh /code/src
ENV PYTHONPATH /code/src

RUN chmod a+x entrypoint.sh
CMD ["./entrypoint.sh"]
