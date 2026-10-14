# 📚 Library Management System

A Dockerized Library Management System built with Python Flask, SQLite, HTML, CSS, and JavaScript.

## Features
- 📖 Browse books with cover images
- 🔍 Search books
- ➕ Add and delete books through REST APIs
- 💾 SQLite database for persistent storage
- 🐳 Docker containerization
- ❤️ Health-check endpoint
- ☁️ Deployed on AWS EC2

## Tech Stack
- Python + Flask
- SQLite
- HTML, CSS, JavaScript
- Docker
- AWS EC2

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/books` | List books |
| GET | `/books` | Retrieve books |
| POST | `/books` | Add a book |
| DELETE | `/books/<id>` | Delete a book |
| GET | `/health` | Check application health |

## Run with Docker

```bash
docker build -t devops-library .
docker run -d --name devops-library-app -p 8001:8000 devops-library
