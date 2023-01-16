FROM balenalib/amd64-alpine-python:build AS build
WORKDIR /remotedaq
COPY ./requirements.txt ./requirements.txt
RUN python -m venv --copies /remotedaq/venv
RUN . /remotedaq/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

FROM balenalib/amd64-alpine-python
COPY --from=build /remotedaq/venv /remotedaq/venv
ENV UDEV=1 PATH=/remotedaq/venv/bin:$PATH
WORKDIR /remotedaq
COPY . ./
CMD python remoteDAQ.py