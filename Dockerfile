FROM python:3.11-slim

# RUN mkdir /telecom
COPY telecom/ /app/telecom

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

WORKDIR /app

CMD ["uvicorn", "telecom.main:app", "--reload"]

LABEL author='Sihuan Newrise' version=1
