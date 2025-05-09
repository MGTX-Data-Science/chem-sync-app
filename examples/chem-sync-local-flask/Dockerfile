FROM python:3.11-slim

# Set environment variables to avoid interactive prompts during installs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required by pip and your packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && pip install --upgrade pip~=23.3.2 setuptools~=69.0.3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./local_app /src/local_app
WORKDIR /src/local_app

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]

