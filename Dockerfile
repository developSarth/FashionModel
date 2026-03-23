# Python slim image for a lightweight container
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Render uses PORT env variable; default to 10000
ENV PORT=10000

# Expose the port
EXPOSE $PORT

# Run the FastAPI app with uvicorn
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
