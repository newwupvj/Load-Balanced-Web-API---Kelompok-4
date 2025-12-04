FROM python:3.9-slim

WORKDIR /app

# Copy requirements dan install library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ .

EXPOSE 5000

CMD ["python", "app.py"]
