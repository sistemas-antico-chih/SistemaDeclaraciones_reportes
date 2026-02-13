import requests
import json
import qrcode
import base64
import io


from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from jinja2 import Environment
from jinja2 import FileSystemLoader
from urllib.parse import urlparse
from weasyprint import CSS
from weasyprint import HTML

from api.generators.custom_filters import boolToSiNo
from api.generators.custom_filters import countryFormat
from api.generators.custom_filters import format_datetime
from api.generators.custom_filters import replacePipe
from api.generators.custom_filters import nationalityFormatPipe
from api.generators.custom_filters import dataEmptyPipe
from api.generators.custom_filters import dateTranslationPipe
# from api.generators.custom_filters import replaceInstitutionPipe


class AcuseDeclaracionGenerator(object):
    def __init__(self, owner: str, institucionData:Dict[str, Any], id: str, data: Dict[str, Any], preliminar: bool = False, publico: bool = False):        
        # print(json.dumps(institucionData,indent=2))
        self.owner:str = owner
        self.institucionData: Dict[str,Any] = institucionData
        self.id: str = id    
        self.data: Dict[str, Any] = data
        self.preliminar = preliminar
        self.publico = publico

    def addJson(self):        
        self.data.update(self.institucionData)
        

    def make_pdf(self):
        env: Environment = Environment(loader=FileSystemLoader('.'))
        env.filters['toSiNo'] = boolToSiNo
        env.filters['formatdatetime'] = format_datetime
        env.filters['countryFormat'] = countryFormat
        env.filters['replace'] = replacePipe
        env.filters['nationalityFormat'] = nationalityFormatPipe
        env.filters['dataEmpty'] = dataEmptyPipe
        env.filters['dateTranslation'] = dateTranslationPipe
        # env.filters['replaceInstitution'] = replaceInstitutionPipe
        templateName = 'templates/acuse_declaracion.html'
        if self.publico:
            templateName = 'templates/publico/acuse_declaracion.html'
        template = env.get_template(templateName)
        self.addJson()
        # 👇 AQUÍ ES DONDE VA
        from datetime import datetime, timezone

        es_extemporanea = False

        tipo = self.data.get("tipoDeclaracion")
        fecha_toma = self.data.get("datosEmpleoCargoComision", {}).get("fechaTomaPosesion")

        fecha_firma = self.data.get("updatedAt")

        if tipo != "MODIFICACION" and fecha_toma and fecha_firma:
            fecha_toma_dt = datetime.strptime(
                fecha_toma, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc)

            fecha_firma_dt = datetime.strptime(
                fecha_firma, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc)

            diferencia_dias = (fecha_firma_dt - fecha_toma_dt).days

            if diferencia_dias >= 61:
                es_extemporanea = True

        # 👇 Se manda al template
        self.data["esExtemporanea"] = es_extemporanea
        
        self.data["qr_code"] = self.generar_qr_base64()
        body_html: str = template.render(self.data)

        # pdf_filename: str = f'reports/acuse-{self.id}.pdf'
        stylesheets: List[CSS] = [CSS(filename='styles/acuse_declaracion.css')]
        if self.preliminar:
            stylesheets.append(CSS(filename='styles/preliminar.css'))
        if self.publico:
            stylesheets.append(CSS(filename='styles/publico.css'))

        return HTML(string=body_html, encoding='utf8').write_pdf(stylesheets=stylesheets)
    

    def generar_qr_base64(self):
        # Construye la URL según el registro
        url = f"https://plataforma.anticorrupcion.org/s1?declara={self.id}"

        # Generar imagen QR
        qr_img = qrcode.make(url)

        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{base64_img}"
