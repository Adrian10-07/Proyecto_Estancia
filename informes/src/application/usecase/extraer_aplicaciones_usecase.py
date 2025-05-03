import re
from typing import List, Dict
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface

class ExtraerAplicacionesUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> List[Dict]:
        texto = self.lector_pdf.leer(ruta_pdf)
        return self._extraer_aplicaciones(texto)

    def _extraer_aplicaciones(self, texto: str) -> List[Dict]:
        apps = []
        matches = re.findall(
            r"([a-zA-Z0-9\-\+ ]+)\s+"                         # nombre de la aplicación
            r"([\d\.]+(?:\s)?(?:[KMG]?bps|[KMG]?BPS))\s+"     # tráfico entrada
            r"([\d\.]+(?:\s)?(?:[KMG]?bps|[KMG]?BPS))\s+"     # tráfico salida
            r"([\d\.]+(?:\s)?(?:[KMG]?bps|[KMG]?BPS))",       # tráfico total
            texto,
            re.IGNORECASE
        )
        print(f"[DEBUG] Matches encontrados: {len(matches)}")

        for match in matches:
            try:
                apps.append({
                    "application": match[0].strip(),
                    "in": self._normalizar_ancho_banda(match[1]),
                    "out": self._normalizar_ancho_banda(match[2]),
                    "total": self._normalizar_ancho_banda(match[3])
                })
            except Exception as e:
                print(f"[ERROR] Aplicación {match[0]} falló con error: {str(e)}")
                continue

        return apps


    def _normalizar_ancho_banda(self, valor: str) -> float:
        valor = str(valor).strip().replace(" ", "").upper()
        
        match = re.match(r"([\d\.]+)([KMG]?BPS)", valor)
        if not match:
            raise ValueError(f"Formato no válido de ancho de banda: '{valor}'")

        numero, sufijo = match.groups()
        numero = float(numero)

        if sufijo == "KBPS":
            return numero * 1_000
        elif sufijo == "MBPS":
            return numero * 1_000_000
        elif sufijo == "GBPS":
            return numero * 1_000_000_000
        elif sufijo == "BPS":
            return numero
        else:
            raise ValueError(f"Unidad desconocida: {sufijo}")