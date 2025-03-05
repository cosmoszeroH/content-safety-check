# Introduction
In this repo, I have created a content safety app that for learning Azure, FastAPI and Docker purpose.
# Folder arrangement
The app folder would be seen like this:
```
│── back-end/
|   ├── Dockerfile
|   ├── requirements.txt
│   ├── main.py
│   ├── .env
│── front-end/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
|   ├── Dockerfile
```
Initially, you have to create an `.env` file in `back-end` folder and add Azure's key and endpoint to this file.

Then, you just have to run `docker-compose up -d` and Docker will automatically run the app for you.
