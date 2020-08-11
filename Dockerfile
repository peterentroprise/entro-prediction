FROM python:3.7.4-stretch

WORKDIR /home/user

# install PDF reader
RUN apt-get update && apt-get install -y poppler-utils
#RUN wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.02.tar.gz && tar -xvf xpdf-tools-linux-4.02.tar.gz && cp xpdf-tools-linux-4.02/bin64/pdftotext /usr/local/bin

# install as a package
COPY setup.py requirements.txt /home/user/
RUN pip install -r requirements.txt
RUN pip install -e .

# copy code
COPY haystack /home/user/haystack
COPY rest_api /home/user/rest_api

# copy saved FARM models
# COPY models* /home/user/models/

# optional : copy sqlite db if needed for testing
#COPY qa.db /home/user/

# optional: copy data directory containing docs for indexing
#COPY data /home/user/data

ENV PORT 8080
EXPOSE 8080

# cmd for running the API
CMD ["gunicorn", "rest_api.application:app",  "-b", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "180"]
