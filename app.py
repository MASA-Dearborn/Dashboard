
import argparse
import json
import sqlite3

from flask import request
from flask import jsonify
from flask import render_template
from flask import Flask

from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

#conn = sqlite3.connect("test_database.db")

"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
db = SQLAlchemy(app)

engine = db.create_engine("sqlite:///test_database.db")
meta = db.MetaData()
meta.reflect(bind=engine)
conn = engine.connect()
"""

tables_list = {}

@app.route('/')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def index():
    return render_template("static/index.html")

@app.route('/config')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def config():
    return jsonify(tables_list)

@app.route('/fetch')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def fetch():
    response = {}
    with sqlite3.connect("test_database.db") as conn:
        for table in tables_list:
            c = conn.cursor()
            c.execute("SELECT * FROM " + table + " ORDER BY id DESC LIMIT 1;")
            response[table] = list(c.fetchone())
        
        #query = meta.tables[table].select().order_by(meta.tables[table].c.id.desc()).limit(1)
        #response[table] = conn.execute(query).fetchall()[0]

    return jsonify(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", type=str, required=True, help="Path to configuration file")

    args = parser.parse_args()

    with open(args.config, "r") as fp:
        config = json.loads(fp.read())["server"]

    tables_list = config["tables"]

    app.run(host=config["ip"], port='5000', debug=True, threaded=True)
