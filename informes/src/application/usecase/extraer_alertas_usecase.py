import re
import json
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface
from datetime import datetime

class ExtraerAlertasUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> dict:
        texto = self.lector_pdf.leer(ruta_pdf)

        # Imprimir
        print("Texto extraído del PDF:")
        print(texto)

        # fecha
        fecha_match = re.search(r"Customer Alerts\s+(.*?)\s+ID", texto)
        generated_at = fecha_match.group(1).strip() if fecha_match else None

        # Periodo
        start_match = re.search(r"Start:(\d{2}/\d{2}/\d{2})", texto)
        end_match = re.search(r"End:(\d{2}/\d{2}/\d{2})", texto)
        start_date = datetime.strptime(start_match.group(1), "%m/%d/%y").strftime("%Y-%m-%dT%H:%M:%S") if start_match else None
        end_date = datetime.strptime(end_match.group(1), "%m/%d/%y").strftime("%Y-%m-%dT%H:%M:%S") if end_match else None

        # Customer info
        customer_id = re.search(r"Customer:(\S+)", texto).group(1)
        name = re.search(rf"{customer_id}\s+(.*?)\s+Ref:", texto).group(1).strip()
        reference = re.search(r"Ref:(.*?)\s+BW", texto).group(1).strip()
        bandwidth = re.search(r"BW:(\S+)", texto).group(1)

        # alertas
        alert_blocks = re.findall(r"(\d{7}.*?)(?=\s{1,7}\d{7}|$)", texto, re.DOTALL)

        # Verificar
        print("Bloques de alertas encontrados:")
        print(alert_blocks)

        alerts = []

        for alert_raw in alert_blocks:
            try:
                id_match = re.search(r"(\d{7})", alert_raw)

                max_impact_match = re.search(r"(\d{1,4}\.\d{1,2}%)", alert_raw)

                throughput_match = re.search(r"(\d{1,4}\.\d{1,2}\s?Mbps,\s?\d{1,4}\.\d{1,2}\s?Kpps)", alert_raw)
                if not throughput_match:
                    throughput_match = re.search(r"(\d{1,4}\.\d{1,2}Mbps.*?)Kpps", alert_raw)

                importance_match = re.search(r"\b(Medium|High|Low)\b", alert_raw)

                alert_type_match = re.search(r"(Incoming .*? Attack)", alert_raw)

                start_time_match = re.search(r"(Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{2}:\d{2} - \d{2}:\d{2}", alert_raw)

                duration_match = re.search(r"\((\d+:\d{2})\)", alert_raw)

                classification_match = re.search(r"(Possible Attack|AS-[A-Z0-9\-]+)", alert_raw)

                annotations_match = re.search(r"(The alert was generated.*?)\)", alert_raw, re.DOTALL)

                alerts.append({
                    "id": id_match.group(1) if id_match else None,
                    "importance": importance_match.group(1) if importance_match else None,
                    "max_impact": max_impact_match.group(1) if max_impact_match else None,
                    "throughput": throughput_match.group(1).replace(" ", "") if throughput_match else None,
                    "alert": alert_type_match.group(1).strip() if alert_type_match else None,
                    "start_time": start_time_match.group(0) if start_time_match else None,
                    "duration": duration_match.group(1) if duration_match else None,
                    "classification": classification_match.group(1) if classification_match else None,
                    "annotations": annotations_match.group(1).replace("\n", " ").strip() + ")" if annotations_match else "No annotations"
                })

            except Exception as e:
                print(f"Error procesando alerta: {e}")
                continue

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
            "alerts": alerts
        }
