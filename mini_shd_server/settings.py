
import os
import imp

# default config
# sqlalchemy database path (if default to false)
DBPath = "sqlite://"
# sqlalcemy echo SQL query
DBEcho = False
# web client echo
WEBEcho = False
# web client host
WEBHost = "0.0.0.0"
# web client port
WEBPort = "5000"
# Max fies for user
FUMax = 100

# raplace default from config file
if "MINI_SHD_CONFIG" in os.environ:
    _conf_name = os.environ["MINI_SHD_CONFIG"]
    if os.path.basename(_conf_name) in os.listdir(os.path.dirname(_conf_name)):
        conf = imp.load_source("conf", os.environ["MINI_SHD_CONFIG"])
        if "DBPath" in conf.__dict__: DBPath = conf.DBPath
        if "DBEcho" in conf.__dict__: DBEcho = conf.DBEcho
        if "WEBEcho" in conf.__dict__: WEBEcho = conf.WEBEcho
        if "WEBHost" in conf.__dict__: WEBHost = conf.WEBHost
        if "WEBPort" in conf.__dict__: WEBPort = conf.WEBPort
        if "FUMax" in conf.__dict__: FUMax = conf.FUMax

# dafault user & jobs settings
init = {
    "user": "admin",
    "passwd": "",
}
