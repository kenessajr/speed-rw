FROM python:3.8-alpine as base
WORKDIR /usr/src/app
COPY setup.py .
RUN pip install -e .
COPY app.py .
CMD ["python", "app.py"]
