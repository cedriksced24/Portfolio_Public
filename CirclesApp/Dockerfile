FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y python3-pyqt5 libgl1-mesa-glx x11-xserver-utils && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "Circles.py"]