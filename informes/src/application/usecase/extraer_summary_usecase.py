import re
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface
from datetime import datetime

class ExtraerSummaryUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> dict:
        texto = self.lector_pdf.leer(ruta_pdf)

        # Fecha
        generated_match = re.search(r"Customer Summary\s+(.*?)\n", texto)
        generated_at = generated_match.group(1).strip() if generated_match else None

        # Periodo
        start_match = re.search(r"Start:\s*(\d{2}/\d{2}/\d{2})", texto)
        end_match = re.search(r"End:\s*(\d{2}/\d{2}/\d{2})", texto)
        start = datetime.strptime(start_match.group(1), "%m/%d/%y").strftime("%Y-%m-%dT%H:%M:%S") if start_match else None
        end = datetime.strptime(end_match.group(1), "%m/%d/%y").strftime("%Y-%m-%dT%H:%M:%S") if end_match else None

        # Cliente
        customer_id = re.search(r"Customer:\s*(\S+)", texto).group(1)
        name_match = re.search(rf"{customer_id}\n(.*?)\s+Ref:", texto)
        name = name_match.group(1).strip() if name_match else "Nombre no encontrado"
        reference = re.search(r"Ref:(.*?)\s+BW", texto).group(1).strip()
        bandwidth = re.search(r"BW:(\S+)", texto).group(1)

        # Datos de tráfico
        metricas = {}
        secciones = ["In", "Out", "Dropped", "Backbone", "Total"]

        for seccion in secciones:
            patron = rf"{seccion}\s+([\d\.]+\s?[KMG]?bps)\s+([\d\.]+\s?[KMG]?bps)\s+([\d\.]+\s?[KMG]?bps)\s+([\d\.]+\s?[KMG]?bps)"
            m = re.search(patron, texto)
            if m:
                metricas[seccion.lower()] = {
                    "current": m.group(1).strip(),
                    "average": m.group(2).strip(),
                    "max": m.group(3).strip(),
                    "percentile_95th": m.group(4).strip()
                }

        return {
            "generated_at": generated_at,
            "period": {
                "start": start,
                "end": end
            },
            "customer_info": {
                "customer_id": customer_id,
                "name": name,
                "reference": reference,
                "bandwidth": bandwidth
            },
            "summary": metricas
        }
