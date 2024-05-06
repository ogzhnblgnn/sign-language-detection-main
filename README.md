# Sign Language Detection

## Installation python-service

### Requirements

```sh
 pip install -r requirements.txt
```
## OR
```sh
pip install opencv-python numpy matplotlib mediapipe scikit-learn tensorflow fastapi
```

## Mobile App
```sh
cd mobile-app
npm install
npm start //expo start
npm android //expo start --android
npm ios //expo start --ios
npm web //expo start --web
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
