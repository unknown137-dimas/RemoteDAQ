FROM python:alpine
RUN pip install -r requirements.txt
CMD runner.sh