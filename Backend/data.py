import re
from typing import Pattern

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
        print(datos_evento)

datos = Data("Guatemala, 20/04/2021 Reportado por: nelson@ing.usac.edu.gt Usuarios afectados: edna@ing.usac.edu.gt, bart@ing.usac.edu.gt Error: 20001 - Desbordamiento de búfer de memoria RAM en el servidor de correo electrónico.")
datos.obtenerDatos()