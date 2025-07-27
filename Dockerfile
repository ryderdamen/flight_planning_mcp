FROM python:3.13-alpine
RUN apk add --no-cache curl
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./
CMD ["python", "main.py"]
