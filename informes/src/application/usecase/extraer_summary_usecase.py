import re
from typing import Dict
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface

class ExtraerSummaryUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> Dict[str, Dict[str, str]]:
        texto = self.lector_pdf.leer(ruta_pdf)
        return self._extraer_metricas(texto)

    def _extraer_metricas(self, texto: str) -> Dict[str, Dict[str, str]]:
        metricas = {}
        secciones = ["In", "Out", "Dropped", "Backbone", "Total"]
        
        for seccion in secciones:
            patron = rf"{seccion}\s+([\d\.]+\s?[KMG]?bps)\s+([\d\.]+\s?[KMG]?bps)\s+([\d\.]+\s?[KMG]?bps)\s+([\d\.]+\s?[KMG]?bps)"
            m = re.search(patron, texto)
            if m:
                metricas[seccion.lower()] = {
                    "current": self._normalizar_valor(m.group(1)),
                    "average": self._normalizar_valor(m.group(2)),
                    "max": self._normalizar_valor(m.group(3)),
                    "percentile_95th": self._normalizar_valor(m.group(4))
                }
        return metricas

    def _normalizar_valor(self, valor: str) -> str:
        return valor.replace(" ", "")