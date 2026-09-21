FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY server.key /app/
COPY server.key.pub /app/
COPY ssh_honeypot.log /app/

RUN chmod 600 server.key

EXPOSE 2222

CMD ["python", "src/ssh_honeypot.py"]
