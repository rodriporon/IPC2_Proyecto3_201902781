import re
import xml.etree.ElementTree as ET
from flask import Flask, json
from flask import jsonify
from flask.globals import request
from flask_cors import CORS
from xml.dom import minidom


global archivo

app = Flask(__name__)
CORS(app)

class Data():
    def __init__(self, evento):
        self.evento = evento

    def obtenerDatos(self):
        datos_evento = {} 
        datos = self.evento
        rcorreo = re.compile('[\w]+@\S+')
        rfecha = re.compile('(?:[0-9]{2}/){2}[0-9]{2}')
        correos = re.findall(rcorreo, datos)
        fechas = re.findall(rfecha, datos)
        datos_evento['fecha'] = fechas
        datos_evento['reportado'] = correos[0]
        datos_evento['afectados'] = correos[1:]
        return datos_evento

@app.route('/', methods=['GET'])
def index():
    return('Api en Flask')

@app.route('/data', methods=['POST'])
def data():
    global archivo
    cantidad_mensajes = {}
    archivo = request.files['archivo']
    tree = ET.parse(archivo)
    root = tree.getroot()
    eventos = []
    for evento in root:
        eventos.append(Data(evento.text).obtenerDatos())
    print(eventos)
    contador = 0
    for evento in eventos:
        for key in evento:
            if key == 'fecha':
                print(f'El key es: {key} y el valor es: {evento[key]}')
                if evento[key][0] in cantidad_mensajes:
                    cantidad_mensajes[evento[key][0]] += 1
                else:
                    cantidad_mensajes[evento[key][0]] = 1
    
    #Creando XML Estadísticas
    raiz_estadisticas = ET.Element('ESTADISTICAS')
    for key in cantidad_mensajes:
        et_estadistica = ET.SubElement(raiz_estadisticas, 'ESTADISTICA')
        et_dato = ET.SubElement(et_estadistica, 'FECHA')
        et_dato2 = ET.SubElement(et_estadistica, 'CANTIDAD_MENSAJES')
        et_dato.text = str(key)
        et_dato2.text = str(cantidad_mensajes[key])
        for evento in eventos:
            if evento['fecha'][0] == key:
                et_dato3 = ET.SubElement(et_estadistica, 'REPORTADO_POR')
                et_dato4 = ET.SubElement(et_dato3, 'USUARIO')
                et_dato5 = ET.SubElement(et_dato4, 'EMAIL')
                et_dato6 = ET.SubElement(et_dato4, 'CANTIDAD_MENSAJES')
                et_dato5.text = str(evento['reportado'])
    xml_estadisticas = ET.tostring(raiz_estadisticas, 'utf-8')
    xml_parseado = minidom.parseString(xml_estadisticas).toprettyxml(indent='\t')
    f = open('estadisticas.xml', 'w')
    f.write(xml_parseado)
    f.close()

                
    print(cantidad_mensajes)
    return ('Leída exitosa')

@app.route('/reset', methods=['GET'])
def reset():
    global archivo
    archivo = None
    return('Api reiniciada')


if __name__ == "__main__":
    app.run(port=5000, debug=True)