FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    libgl1-mesa-dev \
    libgl1-mesa-glx  

RUN pip install opencv-python
RUN pip install numpy
RUN pip install matplotlib
RUN pip install mediapipe
RUN pip install scikit-learn
RUN pip install tensorflow
RUN pip install fastapi
RUN pip install uvicorn

WORKDIR /app

COPY . /app

CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "80"]
