# Notelock
Notelock is a lightweight, secure FastAPI service designed for creating and reading notes safely and anonymously. 📝🔒

## Features
- Encryption
- Automatically deleted after being read

## Getting started
- Clone the repository
```bash
git clone https://github.com/Codi33/notelock
```
- Navigate to the project directory
```bash
cd notelock
```
- Create config file
```bash
cp .env.example .env
```
- Build docker image
```bash
docker build -t notelock .
```
- Run docker container
```bash
docker run -p 80:8000 -d notelock
```
