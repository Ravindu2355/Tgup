# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (not strictly necessary for a Telegram bot)
EXPOSE 80

# Run the bot when the container launches
CMD python3 bot.py
