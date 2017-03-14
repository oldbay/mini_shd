from mini_shd_server import settings

SECRET_KEY = 'CHANGE_ME'
STATIC_ROOT = None
UPLOAD_FOLDER = "/tmp"
SERVER_NAME = "%s:%s"%(settings.WEBHost, settings.WEBPort)
