# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ ./app

# Expose port 5000 for the Flask application
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app/main.py"]
