# TEST

Using dropbox for storing binary data, and redis for work with keys. Redis used to minimize dropbox requests.

## Installing / Getting started

```shell
git clone https://github.com/volodymyr-vereshchak/test-service.git
cd test-service
run redis
initialize enviroment variables, sample: .env.sample
uvicorn api_service.main:app - for run server
127.0.0.1/docs/ - Swagger UI
```
