# Use official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Create directories for static and media
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media

# Copy project
COPY . /app/

# Collect static files

# Expose port
EXPOSE 8000

# Start gunicorn server
CMD ["gunicorn", "BeFriended.wsgi:application", "--bind", "0.0.0.0:8000"]
