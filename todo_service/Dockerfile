# Use a lightweight Python image
FROM python:3.11-slim

# Create a working directory
WORKDIR /app

# Copy requirement file, install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the Flask default port
EXPOSE 5000

# Command to run
CMD ["python", "server.py"]
