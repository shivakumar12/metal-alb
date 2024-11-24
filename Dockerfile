FROM python:3.10.0rc2-alpine
LABEL maintainer="xxxxx"
WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src/ .
CMD ["./gom.py"]
ENTRYPOINT ["python3"]
