FROM python:slim-bullseye

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY xwick-telecom/ /app

WORKDIR /app

CMD ["uvicorn", "telecom.main:app", "--reload"]
