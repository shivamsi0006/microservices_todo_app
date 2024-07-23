# Use Python Alpine base image
FROM python:3.11-alpine

# Install PostgreSQL client and dependencies
RUN apk update \
    && apk add --no-cache postgresql-client postgresql-dev gcc python3-dev musl-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 5000 (adjust if your Flask app runs on a different port)
EXPOSE 5001

# Command to run the application
CMD ["python", "app.py"]
