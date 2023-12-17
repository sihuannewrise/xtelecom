FROM python:3.11.1-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

ADD telecom /app/telecom

CMD ["uvicorn", "telecom.main:app", "--host 0.0.0.0", "--port 8001"]

LABEL copyright='@xwick' version=1
