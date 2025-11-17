FROM python:3.9-slim

WORKDIR /app

COPY .

RUN pip install --no-chace-dir -r requirements.txt

EXPOSE 8087

CMD ["python", "Collect-Websocket.py"]
