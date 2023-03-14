FROM python:3.9

COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt

COPY . /src
RUN python3 /src/manage.py migrate

EXPOSE 6060
WORKDIR src

CMD ["python3", "manage.py", "runserver", "0.0.0.0:6060"]
