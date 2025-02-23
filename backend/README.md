# Installation Guide

Install pixi. Then, run

```
pixi install
```

The deepface, mediapipe library is not found, so we are using:

```
pixi add langchain-community --pypi
pixi add mediapipe --pypi
pixi add deepface --pypi
```

then, source into the workspace with

```
pixi shell
```

How to begin the fastapi server:

```
cd src
uvicorn main:app --reload
```
