from flask_cors import CORS, cross_origin
from app import app


cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from . import client_routes, device_routes