FROM python:3.11.1-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./telecom .

# CMD ["uvicorn", "telecom.main:app", "--reload"]

# LABEL author='Sihuan Newrise' version=1
