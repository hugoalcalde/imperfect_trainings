# Base image
FROM python:3.11-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential git curl gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY imperfect-training.json /root/imperfect-training.json
#COPY requirements.txt requirements.txt
#COPY pyproject.toml pyproject.toml
#COPY imperfect_trainings/ imperfect_trainings/
#COPY dataset/ dataset/
#COPY models/ models/

# Set up Google Cloud SDK and authenticate
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin
#ENV GDRIVE_CREDENTIALS_DATA: ${{secrets.GOOGLECLOUD_KEYS}}
#RUN gcloud auth activate-service-account --key-file=/root/imperfect-training.json
#RUN gcloud auth activate-service-account --key-file=GDRIVE_CREDENTIALS_DATA

# Pass Google Cloud credentials as a build argument
ARG GDRIVE_CREDENTIALS_DATA
ENV GDRIVE_CREDENTIALS_DATA $GDRIVE_CREDENTIALS_DATA
RUN gcloud auth activate-service-account --key-file=$GDRIVE_CREDENTIALS_DATA


# Install DVC
RUN pip install dvc
RUN pip install dvc[gs]

WORKDIR /app

# Copy DVC files
#COPY .dvc/ /app/.dvc/
#COPY data.dvc /app/data.dvc

# Run DVC pull to fetch data
RUN git clone -b clouddvcintegration https://github.com/hugoalcalde/imperfect_trainings.git
#WORKDIR /app/imperfect_trainings
#RUN dvc pull

WORKDIR /app/imperfect_trainings
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install . --no-deps --no-cache-dir
CMD ["tail", "-f", "/dev/null"]
#ENTRYPOINT ["python", "-u", "imperfect_trainings/train_model.py"]
