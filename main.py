import os
# add config file
os.environ["MINI_SHD_CONFIG"] = "%s/mini_shd.cfg"%(
    os.path.dirname(os.path.abspath(__file__))
)
from mini_shd_server import settings
from mini_shd_webclient import app


if __name__ == '__main__':
    app.run(debug=settings.WEBEcho)
