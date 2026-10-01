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
        tipo_declaracion: str,
        declaracion_completa: bool,
        es_extemporanea: bool,
        anio_ejercicio: int,
        nombre: str,
        primer_apellido: str,
        segundo_apellido: str,
        curp: str,
        rfc: str,
        correo_personal: str,
        nombre_ente_publico: str,
        municipio: str,
        seccion: str,
        nota: str,
        fecha: str,
        numero_nota: int,
        titular_oic: str,
        cargo_titular_oic: str
    ):

        self.owner = owner
        self.id = id
        self.tipo_declaracion = tipo_declaracion
        self.declaracion_completa = declaracion_completa
        self.es_extemporanea = es_extemporanea
        self.anio_ejercicio = anio_ejercicio
        self.nombre = nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.curp = curp
        self.rfc = rfc
        self.correo_personal = correo_personal
        self.nombre_ente_publico = nombre_ente_publico
        self.municipio = municipio
        self.seccion = seccion
        self.nota = nota
        self.fecha = fecha
        self.numero_nota = numero_nota
        self.titular_oic = titular_oic
        self.cargo_titular_oic = cargo_titular_oic

    def make_pdf(self):

        env = Environment(
            loader=FileSystemLoader('.')
        )

        template = env.get_template(
            'templates/nota_aclaratoria.html'
        )

        forma = (
            'COMPLETA'
            if self.declaracion_completa
            else 'SIMPLE'
        )

        temporalidad = (
            'EXTEMPORÁNEA'
            if self.es_extemporanea
            else 'ORDINARIA'
        )

        tipo = self.tipo_declaracion

        encabezado = (
            f'ACUSE DE NOTA ACLARATORIA SOBRE LA DECLARACIÓN '
            f'{tipo} {forma} {temporalidad}'
        )

        datos = {
            'id': self.id,
            'numeroNota': self.numero_nota,
            'tipoDeclaracion': tipo,
            'forma': forma,
            'temporalidad': temporalidad,
            'encabezado': encabezado,

            'anioEjercicio': self.anio_ejercicio,

            'nombre': self.nombre,
            'primerApellido': self.primer_apellido,
            'segundoApellido': self.segundo_apellido,

            'nombreCompleto': ' '.join(
                filter(
                    None,
                    [
                        self.nombre,
                        self.primer_apellido,
                        self.segundo_apellido
                    ]
                )
            ),

            'curp': self.curp,
            'rfc': self.rfc,
            'correoPersonal': self.correo_personal,

            'nombreEntePublico': self.nombre_ente_publico,
            'municipio': self.municipio,

            'fecha': self.fecha,
            'seccion': self.seccion,
            'nota': self.nota,

            'titularOIC': self.titular_oic,
            'cargoTitularOIC': self.cargo_titular_oic
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