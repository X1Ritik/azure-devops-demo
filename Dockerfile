# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install dependencies first (layer caching)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app/ .

# Expose port
EXPOSE 8000

# Run with gunicorn (production server)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
