from flask import Flask

app = Flask(__name__)
app.config.from_object('mini_shd_webclient.config')

import hooks
import views
