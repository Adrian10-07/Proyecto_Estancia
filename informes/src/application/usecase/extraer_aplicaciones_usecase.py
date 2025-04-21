import re
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface
from datetime import datetime

class ExtraerAplicacionesUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> dict:
        texto = self.lector_pdf.leer(ruta_pdf)

        # Cliente
        customer_id = re.search(r"Customer:?[\s']*(ECOSU\S+)", texto).group(1)
        name_match = re.search(rf"{customer_id}\s+(.*?)\s+Ref:", texto)
        name = name_match.group(1).strip() if name_match else "Nombre no encontrado"
        reference = re.search(r"Ref:(.*?)\s+BW", texto).group(1).strip()
        bandwidth = re.search(r"BW:(\S+)", texto).group(1)

        # Periodo
        start_match = re.search(r"Start:\s*(\d{2}/\d{2}/\d{2})", texto)
        end_match = re.search(r"End:\s*(\d{2}/\d{2}/\d{2})", texto)
        start = datetime.strptime(start_match.group(1), "%m/%d/%y").strftime("%Y-%m-%dT%H:%M:%S") if start_match else None
        end = datetime.strptime(end_match.group(1), "%m/%d/%y").strftime("%Y-%m-%dT%H:%M:%S") if end_match else None

        # tabla
        apps = []
        matches = re.findall(r"([a-z0-9\-\+ ]+)\s+([\d\.]+(?: [KMG]?bps|[KMG]?bps))\s+([\d\.]+(?: [KMG]?bps|[KMG]?bps))\s+([\d\.]+(?: [KMG]?bps|[KMG]?bps))", texto, re.IGNORECASE)

        for m in matches:
            apps.append({
                "application": m[0].strip(),
                "in": m[1].strip(),
                "out": m[2].strip(),
                "total": m[3].strip()
            })

        return {
            "generated_at": re.search(r"Applications\s+(.*?)\n", texto).group(1).strip(),
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
            "applications": apps
        }