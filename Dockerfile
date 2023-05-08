FROM balenalib/amd64-ubuntu-python
ENV UDEV=1
WORKDIR /rdaq-node
COPY ./Automation/* /rdaq-node
COPY ./requirements.txt /rdaq-node
RUN pip install -r requirements.txt
CMD python remoteDAQ.py