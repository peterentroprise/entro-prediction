FROM  nvidia/cuda:10.1-runtime

WORKDIR /home/user
RUN apt-get update && apt-get install -y python3.7 python3.7-dev python3.7-distutils python3-pip wget curl git poppler-utils

# Set default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN update-alternatives --set python3 /usr/bin/python3.7

# install as a package
COPY setup.py requirements.txt /home/user/
RUN pip3 install -r requirements.txt
RUN pip3 install -e .

# copy code
COPY haystack /home/user/haystack
COPY rest_api /home/user/rest_api

# copy saved FARM models
# COPY models* /home/user/models/

# Optional: copy data directory containing docs for indexing
#COPY data /home/user/data

ENV PORT 8080
EXPOSE 8080

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# cmd for running the API
CMD ["gunicorn", "rest_api.application:app", "-b", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "180"]
