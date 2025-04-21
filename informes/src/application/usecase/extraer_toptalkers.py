import re
import json
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface
from datetime import datetime

class ExtraerTopTalkersUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> dict:
        texto = self.lector_pdf.leer(ruta_pdf)

        
        print("Texto extraído del PDF:")
        print(texto)

        # fecha
        fecha_match = re.search(r"Customer '.*?'\s+Top Talkers External\s+(.*?)\s+DETAILS", texto)
        generated_at = fecha_match.group(1).strip() if fecha_match else None

        # Periodo
        start_match = re.search(r"Start:\s(\d{2}/\d{2}/\d{2})", texto)
        end_match = re.search(r"End:\s(\d{2}/\d{2}/\d{2})", texto)
        start_date = datetime.strptime(start_match.group(1), "%m/%d/%y").strftime("%Y-%m-%dT%H:%M:%S") if start_match else None
        end_date = datetime.strptime(end_match.group(1), "%m/%d/%y").strftime("%Y-%m-%dT%H:%M:%S") if end_match else None

        # Customer info
        customer_match = re.search(r"Customer:\s(.*?)\n", texto)
        customer_id = customer_match.group(1) if customer_match else None

        name_match = re.search(rf"{customer_id}\s+(.*?)\s+Ref:", texto)
        name = name_match.group(1).strip() if name_match else None

        reference_match = re.search(r"Ref:(.*?)\s+BW", texto)
        reference = reference_match.group(1).strip() if reference_match else None

        bandwidth_match = re.search(r"BW:(\S+)", texto)
        bandwidth = bandwidth_match.group(1) if bandwidth_match else None

        # Extraer datos de tráfico
        talkers = []
        talker_blocks = re.findall(r"(\d+\.\d+\.\d+\.\d+)\s+([\d.]+\s(?:Mbps|Kbps))\s+([\d.]+\s(?:Mbps|Kbps))\s+([\d.]+\s(?:Mbps|Kbps))", texto)

        for talker in talker_blocks:
            talkers.append({
                "ip": talker[0],
                "incoming": talker[1],
                "outgoing": talker[2],
                "total": talker[3]
            })

        return {
            "generated_at": generated_at,
            "period": {
                "start": start_date,
                "end": end_date
            },
            "customer_info": {
                "customer_id": customer_id,
                "name": name,
                "reference": reference,
                "bandwidth": bandwidth
            },
            "top_talkers": talkers
        }