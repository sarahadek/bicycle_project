# 1. Use a lightweight Python image
FROM python:3.12-slim AS builder

# 2. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Set the working directory
WORKDIR /app

# 4. Copy your dependency files
COPY pyproject.toml uv.lock ./

# 5. Install dependencies into a virtual environment
RUN uv sync --frozen --no-cache

# --- Final Stage ---
FROM python:3.12-slim

WORKDIR /app

# 6. Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv
COPY . .

# 7. Make sure we use the virtual environment's python
ENV PATH="/app/.venv/bin:$PATH"

# 8. Run your main script
CMD ["python", "main.py"]