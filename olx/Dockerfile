# Use official Python image
FROM python:3.12-slim



# Set work directory
WORKDIR /app

# Install dependencies

COPY requirements.txt /app
RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN pip install -r /app/requirements.txt


# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run the app
CMD ["gunicorn", "olx.wsgi:application", "--bind", "0.0.0.0:8000"]
