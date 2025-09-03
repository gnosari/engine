FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create virtual environment (use system Python)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy source code
COPY src/ ./src/
COPY examples/ ./examples/

# Create db directory for knowledge bases
RUN mkdir -p db

# Set Python path
ENV PYTHONPATH=/app

# Default command
CMD ["poetry", "run", "gnosari", "--help"]
