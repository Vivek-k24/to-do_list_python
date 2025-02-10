FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# This service doesn't expose an HTTP port (unless you want an API),
# so we won't EXPOSE anything here. It's just an internal worker.

CMD ["python", "reminder_service.py"]
