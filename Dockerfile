# Use the official lightweight Python image
FROM python:3.10-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Create and activate a Python virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask (if needed, optional for Telegram bots)
EXPOSE 5000

# Run the bot
CMD ["python", "bot.py"]
