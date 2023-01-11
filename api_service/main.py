import dropbox

from fastapi import FastAPI, UploadFile, Response, status

from .dropbox_serv import DropboxService
from .redis_serv import RedisService

app = FastAPI()

@app.put("/", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile, key: str, response: Response):
    redis_serv = RedisService()
    with DropboxService(key) as dbx_serv:
        try:
            dbx_serv.upload_file(file, redis_serv.check_key(key))
        except dropbox.exceptions.ApiError:
            response.status_code = status.HTTP_400_BAD_REQUEST
        else:
            redis_serv.set_key(key)

@app.get("/", status_code=status.HTTP_200_OK)
async def get_data_by_key(key: str, response: Response) -> str|None:
    redis_serv = RedisService()
    if redis_serv.get_key(key) is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Key not found!"
    with DropboxService(key) as dbx_serv:
        try:
            dbx_serv.download_file()
        except dropbox.exceptions.ApiError:
            response.status_code = status.HTTP_400_BAD_REQUEST
