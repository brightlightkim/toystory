# Installation Guide

Install pixi. Then, run

```
pixi install
```

The deepface library is not found, so we are using:

```
pip install deepface
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
