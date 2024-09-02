docker build -t barksend:latest .
docker save -o barksend.tar barksend
docker run -p 8000:8000 --name barksend -d barksend:latest
