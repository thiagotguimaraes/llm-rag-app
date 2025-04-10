cd services/user-service
docker build -t user-service .
docker run -p 8000:8000 user-service