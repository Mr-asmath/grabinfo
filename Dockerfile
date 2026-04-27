cd D:\program\python\grabinfo-main

# Remove the bad Dockerfile if it exists
Remove-Item Dockerfile -ErrorAction SilentlyContinue

# Create correct Dockerfile
@"
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# Set work directory
WORKDIR /app

# Install system dependencies for Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Create media directory
RUN mkdir -p /app/media

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start command
CMD ["gunicorn", "grabinfo.wsgi:application", "--bind", "0.0.0.0:8000"]
"@ | Out-File -FilePath Dockerfile -Encoding utf8 -NoNewline
