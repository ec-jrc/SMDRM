FROM python:3.8-alpine
RUN python -m pip install --upgrade pip pytest requests
WORKDIR /upload_test
COPY test_data.zip .
COPY test_upload.py .
CMD python -m pytest .
