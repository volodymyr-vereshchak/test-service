import os
from dotenv import load_dotenv

load_dotenv()

# dropbox settings
OAUTH2_REFRESH_TOKEN = os.getenv("OAUTH2_REFRESH_TOKEN")
APP_SECRET = os.getenv("APP_SECRET")
APP_KEY = os.getenv("APP_KEY")
DROPBOX_PATH = "/test-service/"
MB_SIZE = 150 * 1024 * 1024
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_PATH = os.path.join(ROOT_DIR, 'download/')

# redis settings
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS = os.getenv("REDIS_PASS")