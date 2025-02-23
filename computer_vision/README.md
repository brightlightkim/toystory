# Facial Emotion Analysis API

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
gunicorn main:app --bind 127.0.0.1:8080
```

3. Test with an image (in new terminal):
```bash
curl -X POST http://127.0.0.1:8080/process_image -F "image=@test.jpg"
```

## Note

Place test images in the project directory. Server runs on localhost:8000.

Author: Ujjwal Gupta
