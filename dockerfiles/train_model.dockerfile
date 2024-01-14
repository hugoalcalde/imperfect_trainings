# Base image
FROM python:3.11-slim

# Install DVC dependencies
#RUN apt update && \
#    apt install --no-install-recommends -y \
#        build-essential \
#        gcc \
#        git \
#        && apt clean && rm -rf /var/lib/apt/lists/*

# Install DVC
RUN pip install dvc
RUN pip install dvc[gs]
# Set up Google Cloud SDK and authenticate
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://sdk.cloud.google.com | bash &&\
    gcloud auth activate-service-account --key-file=imperfect-training-a827b028141a.json && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Set working directory
WORKDIR /

# Copy DVC files
COPY .dvc/ .dvc/

# Run DVC pull to fetch data
RUN dvc pull
