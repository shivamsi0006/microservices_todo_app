# Use Python Alpine base image
FROM python:3.11-alpine

# Install dependencies
RUN apk update \
    && apk add --no-cache git postgresql postgresql-client postgresql-dev gcc python3-dev musl-dev su-exec

# # Set environment variables for PostgreSQL  to specify the location of the PostgreSQL data directory.
ENV PGDATA=/var/lib/postgresql/data   

# Create necessary directories and set permissions
RUN mkdir -p /var/lib/postgresql/data /var/run/postgresql \
    && chown -R postgres:postgres /var/lib/postgresql /var/run/postgresql

# Switch to the postgres user
USER postgres

# Initialize the PostgreSQL database
RUN initdb -D /var/lib/postgresql/data

# Create the database
RUN pg_ctl start -D /var/lib/postgresql/data &&\
    psql --command "CREATE DATABASE database;" &&\
    pg_ctl stop -D /var/lib/postgresql/data

# Switch back to root to install Python dependencies
USER root

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 5000 (adjust if your Flask app runs on a different port)
EXPOSE 5000

# Expose port 5432 for PostgreSQL
EXPOSE 5432

# Command to start PostgreSQL and the Flask application
CMD su-exec postgres sh -c "pg_ctl start -D /var/lib/postgresql/data & python app.py"
