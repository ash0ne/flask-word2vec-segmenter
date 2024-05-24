# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install gcc g++ -y
RUN pip install --no-cache-dir -r requirements.txt

# Uncomment to install dependencies behind proxy
# RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Set environment variables for Flask app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set environment variables for user credentials and secret key
# These can be overridden when running the container
ENV APP_USER=admin
ENV APP_PASSWORD=adminpass
ENV SECRET_KEY=your_secret_key

# Expose port 5000 for the Flask app to run on
EXPOSE 5000

# Define volume for uploads
VOLUME [ "/app/uploads" ]

# Start gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]