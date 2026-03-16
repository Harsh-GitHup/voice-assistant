FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Install system build dependencies for pyaudio, opencv, and espeak
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential=12.9.1 \
    portaudio19-dev=19.6.0-1.2 \
    libasound2-dev=1.2.9-2+deb12u1 \
    libgl1-mesa-glx=23.2.1-1 \
    espeak-ng-data=1.51-2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Enable bytecode compilation for faster startups
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON=python3.11

# Copy lockfiles and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Final Stage
FROM python:3.11-slim-bookworm

WORKDIR /app

# Runtime libraries for Audio/CV and essential tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    libportaudio2=19.6.0-1.2 \
    libasound2=1.2.9-2+deb12u1 \
    libglib2.0-0=2.74.6-12 \
    libgl1-mesa-glx=23.2.1-1 \
    espeak-ng=1.51-2 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app && useradd --system --gid app --create-home app

# Copy the virtual environment from the builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy project files
COPY --chown=app:app main.py generate_test_audio.py ./
COPY --chown=app:app .env.example ./
COPY --chown=app:app README.md LICENSE ./

# Use the virtual env by default
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check validates main.py imports (not execution)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import main; print('healthy')" || exit 1

USER app

# Default to CLI assistant
CMD ["python", "main.py"]