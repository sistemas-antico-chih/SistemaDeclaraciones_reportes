import io

from datetime import datetime
from typing import Any, Dict

from jinja2 import Environment
from jinja2 import FileSystemLoader
from weasyprint import CSS
from weasyprint import HTML


class NotaAclaratoriaGenerator(object):

    def __init__(
        self,
        owner: Dict[str, Any],
        id: str,
        seccion: str,
        nota: str,
        fecha: str
    ):
        self.owner = owner
        self.id = id
        self.seccion = seccion
        self.nota = nota
        self.fecha = fecha

    def make_pdf(self):

        env: Environment = Environment(
            loader=FileSystemLoader('.')
        )

        template = env.get_template(
            'templates/nota_aclaratoria.html'
        )

        nombre = ' '.join(
            filter(
                None,
                [
                    self.owner.get('nombre'),
                    self.owner.get('primerApellido'),
                    self.owner.get('segundoApellido')
                ]
            )
        )

        datos = {
            'id': self.id,
            'nombre': nombre,
            'fecha': self.fecha,
            'seccion': self.seccion,
            'nota': self.nota
        }

        body_html = template.render(datos)

        stylesheets = [
            CSS(
                filename='styles/nota_aclaratoria.css'
            )
        ]

        return HTML(
            string=body_html,
            encoding='utf8'
        ).write_pdf(
            stylesheets=stylesheets
        )