#!/usr/bin/python
import logging
from logging.handlers import RotatingFileHandler
from app import app

# Configuration
HOST = '192.168.1.35'
PORT = 5000
LOG_FILENAME = 'qrcode-to-pdf'

# Logger
formatter = logging.Formatter(
    "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Run the app
app.run(host=HOST, port=PORT)
