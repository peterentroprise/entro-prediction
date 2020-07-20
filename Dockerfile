FROM  nvidia/cuda:10.1-runtime

WORKDIR /home/user

RUN apt-get update && apt-get install -y python3.7 python3.7-dev python3.7-distutils python3-pip wget curl git

# Set default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN update-alternatives --set python3 /usr/bin/python3.7

# copy code
COPY haystack /home/user/haystack
COPY rest_api /home/user/rest_api

# install pdf reader
RUN wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.02.tar.gz && tar -xvf xpdf-tools-linux-4.02.tar.gz && cp xpdf-tools-linux-4.02/bin64/pdftotext /usr/local/bin

# install as a package
COPY setup.py requirements.txt /home/user/
RUN pip3 install -r requirements.txt
RUN pip3 install -e .

# copy saved FARM models
# COPY models* /home/user/models/

# Optional: copy sqlite db if needed for testing
#COPY qa.db /home/user/

# Optional: copy data directory containing docs for indexing
#COPY data /home/user/data

EXPOSE 8080

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8


# cmd for running the API
CMD ["gunicorn", "haystack.api.application:app", "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "2", "--timeout", "180"]