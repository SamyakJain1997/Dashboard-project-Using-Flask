#used for Report process Funtion TAC3 Report Process OPTICS_TAC3

from flask import Flask

UPLOAD_FOLDER = './static/upload'

application = Flask(__name__)
application.secret_key = "secret key"
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

