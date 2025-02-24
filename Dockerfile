FROM python:3.9-slim

WORKDIR /home/python

RUN apt update && apt install -y build-essential findutils

# If using postgres:
#RUN apt install -y postgresql-common libpq-dev

# If using mysql/mariadb:
#RUN apt update && apt install -y default-mysql-client libmariadb-dev pkg-config

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

CMD ["bash"]

