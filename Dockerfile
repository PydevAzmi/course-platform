# Strat Docker : Python + Kernal
FROM python:3.12-slim-bullseye

# ENV: Show Logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create Project Folder 
WORKDIR /code

# Copy Requirements
COPY requirements.txt /code/requirements.txt

# Install Requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Code > Docker
COPY . /code/