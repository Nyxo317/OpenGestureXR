FROM python:3.11-slim

WORKDIR /app

# OpenCV runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai_engine/ ai_engine/
COPY gesture_api/ gesture_api/

EXPOSE 8000

CMD ["uvicorn", "gesture_api.server.main:app", "--host", "0.0.0.0", "--port", "8000"]
