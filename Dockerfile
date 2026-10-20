FROM python:3.12-slim

WORKDIR /app

# The core server has zero external dependencies!
# Optionally install fastapi & uvicorn if needed:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

COPY . .

EXPOSE 8000

# Runs zero-dependency pure Python server by default
CMD ["python3", "-m", "app.main", "8000"]
