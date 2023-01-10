import os
import dropbox

from concurrent.futures import ThreadPoolExecutor
from settings import(
    OAUTH2_REFRESH_TOKEN,
    APP_KEY,
    APP_SECRET,
    DROPBOX_PATH,
    MB_SIZE,
    DOWNLOAD_PATH
)

class DropboxService:
    def __init__(self, key: str) -> None:
        self.dbx = dropbox.Dropbox(
            oauth2_refresh_token=OAUTH2_REFRESH_TOKEN,
            app_secret=APP_SECRET,
            app_key=APP_KEY
        )
        self.path = f"{DROPBOX_PATH}{key}"
        self.download_path = f"{DOWNLOAD_PATH}{key}"
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.dbx.close()


    def upload_file(self, file, write_mode: bool):
        file_size = os.fstat(file.file.fileno()).st_size
        mode = dropbox.files.WriteMode.overwrite if write_mode else dropbox.files.WriteMode.add
        if file_size <= MB_SIZE:
            self.dbx.files_upload(file.file.read(), self.path, mode=mode)
        else:
            data = file.file.read(MB_SIZE)
            session_start_result = self.dbx.files_upload_session_start(data, close=file.file.tell() == file_size)
            while file.file.tell() < file_size - MB_SIZE:
                cursor = dropbox.files.UploadSessionCursor(session_id=session_start_result.session_id, offset=file.file.tell())
                data = file.file.read(MB_SIZE)                
                self.dbx.files_upload_session_append_v2(
                    file.file.read(MB_SIZE),
                    cursor=cursor,
                    close=file.file.tell() == file_size
                )
            cursor = dropbox.files.UploadSessionCursor(session_id=session_start_result.session_id, offset=file.file.tell())
            data = file.file.read(MB_SIZE)            
            commit = dropbox.files.CommitInfo(path=self.path, mode=mode)
            self.dbx.files_upload_session_finish(f=data, cursor=cursor, commit=commit)


    def download_file(self):
        self.dbx.files_download_to_file(self.download_path, self.path)
