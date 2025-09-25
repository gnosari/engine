wFROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* README.md  ./
COPY src/ ./src/
COPY examples/ ./examples/

# Configure Poetry to not create virtual environment (use system Python)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install

# Copy source code


# Create db directory for knowledge bases
RUN mkdir -p db

# Set Python path
ENV PYTHONPATH=/app

# Default command
CMD ["poetry", "run", "gnosari", "--help"]
