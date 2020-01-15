
import sqlalchemy as db

from flask import request
from flask import jsonify
from flask import Flask

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

engine = db.create_engine("sqlite:///database.db")
meta = db.MetaData()
meta.reflect(bind=engine)
conn = engine.connect()

@app.route('/fetch', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def fetch():
    message = request.get_json(force=True)
    name = message['name']
    response = {
        'data': 'Hello, ' + name + '!'
    }

    #
    return jsonify(response)
