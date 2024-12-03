# Use official Python image as a base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv (or use virtualenv if preferred)
RUN pip install --no-cache-dir pipenv

# Copy only the requirements file for caching purposes
COPY requirements.txt /app/

# Install Python dependencies in a virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port Django will run on
EXPOSE 8000

# Set environment variables for Django
ENV SECRET_KEY=your_secret_key_here
ENV DEBUG=False
ENV HOST=0.0.0.0
ENV PORT=8000
ENV BEACON_API_URL=http://127.0.0.1:5050/api/g_variants

# Command to run the application
CMD ["python", "manage.py", "runserver"]
