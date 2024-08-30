FROM python:3.12.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

ADD app /app/telecom

CMD ["uvicorn", "telecom.main:app", "--host=0.0.0.0"]

LABEL copyright='@xwick'
