# Sign Language Detection

## Installation python-service

### Requirements

```sh
pip install opencv-python numpy matplotlib mediapipe scikit-learn tensorflow fastapi
```

### Predict API

```sh
cd python-service
py -m uvicorn predict:app
```

### Docker Installation

```sh
cd python-service
docker pull tiangolo/uvicorn-gunicorn-fastapi
docker build -t myapp .
docker run -p 80:80 myapp
```
