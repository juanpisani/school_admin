# Use the latest Python 3.12 slim image
FROM --platform=linux/amd64 python:3.12.9-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install the application dependencies using pip
# --no-cache-dir reduces the size of the image
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Expose the port that the application listens on
EXPOSE 8000

# Set the environment variable for Django settings (if needed)
# ENV DJANGO_SETTINGS_MODULE=your_project.settings

# Define the command to start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Add non-root user to container
RUN groupadd -r app && useradd -r -g app app
USER app
