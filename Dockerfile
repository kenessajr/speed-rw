FROM python:3.8-alpine as base
WORKDIR /usr/src/app
COPY setup.py .
RUN apk update && \
    apk add tesseract-ocr && \
    apk add libtesseract-dev && \
    pip install -e .
COPY app.py .
CMD ["python", "app.py"]
