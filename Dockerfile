# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port Flask runs on
EXPOSE 5000

# Set the environment variable to avoid Python buffering
ENV PYTHONUNBUFFERED 1

# Run the Flask app
CMD ["python", "app.py"]

