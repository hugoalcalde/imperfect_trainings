# Base image
FROM python:3.11-slim

# Install DVC dependencies
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the service account key file
COPY imperfect-training-a827b028141a.json /root/imperfect-training-a827b028141a.json
# Debugging: Check if the file is present
RUN ls -l /root/imperfect-training-a827b028141a.json

# Set up Google Cloud SDK and authenticate
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin
RUN gcloud auth activate-service-account --key-file=/root/imperfect-training-a827b028141a.json

# Install DVC
RUN pip install dvc
RUN pip install dvc[gs]

# Set working directory to a directory inside a Git repository
WORKDIR /app

# Copy DVC files
COPY .dvc/ /app/.dvc/

# Run DVC pull to fetch data
RUN git init && \
    dvc pull
CMD ["tail", "-f", "/dev/null"]
