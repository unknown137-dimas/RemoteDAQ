FROM balenalib/amd64-alpine-python
ENV UDEV=1
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD python remoteDAQ.py