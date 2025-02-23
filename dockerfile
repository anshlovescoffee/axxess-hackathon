FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    flask==2.0.1 \
    flask-cors==3.0.10 \
    psycopg2==2.9.3 \
    requests==2.25.1 \
    pycryptodome==3.10.1 \
    Werkzeug==2.0.3

# Copy the application code
COPY app.py .

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
CMD ["python", "app.py"]