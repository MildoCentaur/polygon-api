FROM python:latest
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . ./app
COPY app.py .
CMD ["python3", "app.py"]