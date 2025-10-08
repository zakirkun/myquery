# Multi-stage build untuk MyQuery
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user -r requirements.txt

# Copy application code
COPY . .

# Install application
RUN pip install --user -e .

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 myquery && \
    mkdir -p /home/myquery/.myquery && \
    chown -R myquery:myquery /home/myquery

# Set working directory
WORKDIR /home/myquery

# Copy installed packages from builder
COPY --from=builder --chown=myquery:myquery /root/.local /home/myquery/.local
COPY --from=builder --chown=myquery:myquery /app /home/myquery/app

# Switch to non-root user
USER myquery

# Set PATH
ENV PATH=/home/myquery/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD myquery --version || exit 1

# Default command
ENTRYPOINT ["myquery"]
CMD ["--help"]

