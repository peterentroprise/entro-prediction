FROM tiangolo/uvicorn-gunicorn-machine-learning:python3.7

ENV TIMEOUT 1000

ENV GRACEFUL_TIMEOUT 1000

RUN conda install -c conda-forge fastapi

RUN conda install pandas tqdm

RUN conda install pytorch cudatoolkit=10.1 -c pytorch

RUN git clone https://github.com/NVIDIA/apex

RUN pip install -v --no-cache-dir ./apex

RUN pip install simpletransformers

RUN pip install transformers

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

COPY ./service-account.json /app

ENV GOOGLE_APPLICATION_CREDENTIALS="service-account.json"

RUN gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

# Copy blank outputs/ folder for a target.

COPY ./app/outputs /app/outputs

# Copy model to outputs/
RUN gsutil cp -R gs://entro-prediction-models /app/outputs

COPY ./app /app