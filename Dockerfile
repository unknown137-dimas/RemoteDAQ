FROM balenalib/amd64-ubuntu-python
ENV UDEV=1
WORKDIR /rdaq-node
COPY . /rdaq-node
RUN chmod +x scripts/driver_install.sh && ./scripts/driver_install.sh
RUN pip install -r requirements.txt
CMD python remoteDAQ.py