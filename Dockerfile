# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install dependencies directly without virtualenv
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make run.sh executable
RUN chmod +x run.sh

# Expose the application port (adjust if needed)
EXPOSE 8000 

# Set environment variables for Flask
ENV FLASK_APP=core/server.py
ENV FLASK_ENV=development 

# Run the database migration commands before starting the application
RUN rm -f core/store.sqlite3
RUN flask db upgrade -d core/migrations/

# Start the server using run.sh
ENTRYPOINT ["bash", "run.sh"]