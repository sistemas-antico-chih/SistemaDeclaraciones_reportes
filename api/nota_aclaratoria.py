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
                seccion=raw_data['seccion'],
                nota=raw_data['nota'],
                fecha=raw_data['fecha']
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