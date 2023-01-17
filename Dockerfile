FROM balenalib/amd64-alpine-python
ENV UDEV=1
WORKDIR /rdaq-node
COPY . /rdaq-node/
RUN pip install -r requirements.txt
CMD python remoteDAQ.py