import xml.etree.ElementTree as ET
from flask import Flask, json
from flask import jsonify
from flask.globals import request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return('Api en Flask')

@app.route('/data', methods=['POST'])
def data():
    archivo = request.files['archivo']
    tree = ET.parse(archivo)
    root = tree.getroot()
    eventos = []
    for evento in root:
        eventos.append(evento)
    return ('Leída exitosa')

if __name__ == "__main__":
    app.run(port=5000, debug=True)