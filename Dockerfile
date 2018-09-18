FROM python:2
COPY . /opt/app
WORKDIR /opt/app
RUN export LD_LIBRARY_PATH='/opt/app/testdir'
# sudo apt-get install python-pip python-dev build-essential ?
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python -m SimpleHTTPServer
