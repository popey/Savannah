FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt update \
    && apt install -y --no-install-recommends \
        build-essential \
        findutils \
    && groupadd -r django \
    && useradd -r -g django django \
    && mkdir -p /app/media /var/lib/sqlite \
    && chown -R django:django /app /var/lib/sqlite \
    && chmod 777 /var/lib/sqlite

# If using postgres:
RUN apt update \
    && apt install -y postgresql-common libpq-dev

# If using mysql/mariadb:
#RUN apt update \
#    && apt install -y default-mysql-client libmariadb-dev pkg-config

# Required by pillow
RUN apt update \
    && apt install -y libjpeg62-turbo-dev zlib1g-dev

# Cleanup apt
RUN rm -rf /var/lib/apt/lists/* \
    && apt clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
RUN chown -R django:django /app

# Switch to django user
USER django

# Command to run
CMD ["bash"]
