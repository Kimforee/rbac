# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Run migrations (if any) and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose the port Django will run on
EXPOSE 8000

# Start the Django app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rbac.wsgi:application"]