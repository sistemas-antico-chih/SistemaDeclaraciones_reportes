import logging

from decouple import config
from typing import Any, Dict

from flask import request
from flask import make_response

from flask_restful.reqparse import RequestParser
from flask_restful import Resource

from api.generators.nota_aclaratoria import NotaAclaratoriaGenerator


class NotaAclaratoria(Resource):

    def __init__(self):

        self.parser = RequestParser(
            bundle_errors=True
        )

        self.parser.add_argument(
            'owner',
            type=dict,
            required=True,
            help='owner is required'
        )

        self.parser.add_argument(
            'id',
            type=str,
            required=True,
            help='id is required'
        )

        self.parser.add_argument(
            'seccion',
            type=str,
            required=True,
            help='seccion is required'
        )

        self.parser.add_argument(
            'nota',
            type=str,
            required=True,
            help='nota is required'
        )

        self.parser.add_argument(
            'fecha',
            type=str,
            required=True,
            help='fecha is required'
        )
        
        self.parser.add_argument('tipoDeclaracion', type=str, required=True, help='tipoDeclaracion is required')
        self.parser.add_argument('declaracionCompleta', type=bool, required=True, help='declaracionCompleta is required')
        self.parser.add_argument('esExtemporanea', type=bool, required=True, help='esExtemporanea is required')
        self.parser.add_argument('anioEjercicio', type=int, required=True, help='anioEjercicio is required')
        self.parser.add_argument('nombre', type=str, required=True, help='nombre is required')
        self.parser.add_argument('primerApellido', type=str, required=True, help='primerApellido is required')
        self.parser.add_argument('segundoApellido', type=str, required=False, default='')
        self.parser.add_argument('curp', type=str, required=True, help='curp is required')
        self.parser.add_argument('rfc', type=str, required=True, help='rfc is required')
        self.parser.add_argument('correoPersonal', type=str, required=True, help='correoPersonal is required')
        self.parser.add_argument('nombreEntePublico', type=str, required=True, help='nombreEntePublico is required')
        self.parser.add_argument('municipio', type=str, required=True, help='municipio is required')
        self.parser.add_argument('numeroNota', type=int, required=True, help='numeroNota is required')
        self.parser.add_argument('titularOIC', type=str, required=True, help='titularOIC is required')
        self.parser.add_argument('cargoTitularOIC', type=str, required=True, help='cargoTitularOIC is required')

    def post(self):

        API_KEY: str = config(
            'API_KEY',
            default=''
        )

        if request.headers.get('X-Api-Key') != API_KEY:

            logging.error(
                'Unauthorized Intent with API_KEY'
            )

            return {
                'success': False,
                'message': 'BAD REQUEST'
            }, 400

        try:

            raw_data: Dict[str, Any] = (
                self.parser.parse_args()
            )

            report = NotaAclaratoriaGenerator(
                owner=raw_data['owner'],
                id=raw_data['id'],
                tipo_declaracion=raw_data['tipoDeclaracion'],
                declaracion_completa=raw_data['declaracionCompleta'],
                es_extemporanea=raw_data['esExtemporanea'],
                anio_ejercicio=raw_data['anioEjercicio'],
                nombre=raw_data['nombre'],
                primer_apellido=raw_data['primerApellido'],
                segundo_apellido=raw_data['segundoApellido'],
                curp=raw_data['curp'],
                rfc=raw_data['rfc'],
                correo_personal=raw_data['correoPersonal'],
                nombre_ente_publico=raw_data['nombreEntePublico'],
                municipio=raw_data['municipio'],
                seccion=raw_data['seccion'],
                nota=raw_data['nota'],
                fecha=raw_data['fecha'],
                numero_nota=raw_data['numeroNota'],
                titular_oic=raw_data['titularOIC'],
                cargo_titular_oic=raw_data['cargoTitularOIC']
            )

            pdf = report.make_pdf()

            response = make_response(pdf)

            response.headers.set(
                'Content-Type',
                'application/pdf'
            )

            return response

        except Exception as e:

            logging.exception(e)

            return {
                'success': False,
                'message': 'BAD REQUEST'
            }, 400