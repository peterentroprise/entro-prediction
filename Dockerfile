FROM tiangolo/uvicorn-gunicorn-machine-learning:python3.7

ENV TIMEOUT 1000

ENV GRACEFUL_TIMEOUT 1000

RUN conda install -c conda-forge fastapi

RUN conda install pandas tqdm

RUN conda install pytorch cudatoolkit=10.1 -c pytorch

RUN git clone https://github.com/NVIDIA/apex

RUN pip install -v --no-cache-dir ./apex

RUN pip install simpletransformers

COPY ./app /app