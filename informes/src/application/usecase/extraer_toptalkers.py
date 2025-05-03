import re
from typing import List, Dict
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface

class ExtraerTopTalkersUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> List[Dict[str, str]]:
        texto = self.lector_pdf.leer(ruta_pdf)
        return self._extraer_toptalkers(texto)

    def _extraer_toptalkers(self, texto: str) -> List[Dict[str, str]]:
        talkers = []
        talker_blocks = re.findall(
            r"(\d+\.\d+\.\d+\.\d+)\s+"  # IP
            r"([\d.]+\s?[KM]?bps)\s+"   # Incoming
            r"([\d.]+\s?[KM]?bps)\s+"   # Outgoing
            r"([\d.]+\s?[KM]?bps)",     # Total
            texto
        )

        for ip, incoming, outgoing, total in talker_blocks:
            talkers.append({
                "ip": ip,
                "incoming": self._normalizar_trafico(incoming),
                "outgoing": self._normalizar_trafico(outgoing),
                "total": self._normalizar_trafico(total)
            })
        
        return talkers

    def _normalizar_trafico(self, valor: str) -> str:
        return valor.replace(" ", "")