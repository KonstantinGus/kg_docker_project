
FROM python:3.12-slim

WORKDIR /kg-app

RUN pip install --no-cache-dir psycopg[binary]

COPY server.py .

EXPOSE 5000

CMD ["python", "server.py"]
