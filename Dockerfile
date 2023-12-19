FROM python:3.11.1-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

ADD xwick/telecom /app/xwick/telecom

CMD ["uvicorn", "xwick.telecom.main:app"]

LABEL copyright='@xwick' version=1
