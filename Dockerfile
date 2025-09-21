# ---- Stage 1: The Builder ----
# This stage installs dependencies into a virtual environment.
FROM python:3.12-slim-bookworm AS builder

# Set build arguments for user and group IDs with a default of 1000
ARG UID=1000
ARG GID=1000

# Set environment variables to prevent writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install uv, the fast Python package installer
RUN pip install uv

# Create a non-root user for security using the build arguments
RUN addgroup --system --gid ${GID} appgroup && \
    adduser --system --uid ${UID} --ingroup appgroup appuser

# Create a virtual environment
RUN uv venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the project definition file and install dependencies
WORKDIR /app
COPY pyproject.toml .
RUN uv pip install --no-cache -e .

# ---- Stage 2: The Final Image ----
# This stage builds the final, lean image for production.
FROM python:3.12-slim-bookworm AS final

# Set build arguments again for the final stage
ARG UID=1000
ARG GID=1000

# Create the same non-root user as in the builder stage
RUN addgroup --system --gid ${GID} appgroup && \
    adduser --system --uid ${UID} --ingroup appgroup appuser

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code into the container
COPY . .

# Grant ownership of the app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Switch to the non-root user
USER appuser
