import re
from typing import List, Dict
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface

class ExtraerAlertasUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> List[Dict]:
        texto = self.lector_pdf.leer(ruta_pdf)
        alert_blocks = self._extraer_bloques_alertas(texto)
        print(f"Bloques encontrados: {len(alert_blocks)}")

        procesadas = []
        for i, alert_raw in enumerate(alert_blocks):
            alerta = self._procesar_alerta(alert_raw)
            if "error" in alerta:
                print(f"[!] Error en bloque {i+1}: {alerta['error']}")
                print(f"    Texto bruto: {alerta['raw_text']}")
            else:
                procesadas.append(alerta)

        print(f"Alertas válidas procesadas: {len(procesadas)}")
        return procesadas



    def _extraer_bloques_alertas(self, texto: str) -> List[str]:
        return re.findall(r"\d{7}.*?(?=\s*\d{7}|\Z)", texto, re.DOTALL)



    def _procesar_alerta(self, alert_raw: str) -> Dict:
        try:
            return {
                "id": self._extraer_valor(r"(\d{7})", alert_raw),
                "importance": self._extraer_valor(r"\b(Medium|High|Low)\b", alert_raw),
                "max_impact": self._extraer_valor(r"(\d{1,4}\.\d{1,2}%)", alert_raw),
                "throughput": self._extraer_throughput(alert_raw),
                "alert": self._extraer_valor(r"(Incoming .*? Attack)", alert_raw),
                "start_time": self._extraer_valor(
                    r"(Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{2}:\d{2} - \d{2}:\d{2}", 
                    alert_raw
                ),
                "duration": self._extraer_valor(r"\((\d+:\d{2})\)", alert_raw),
                "classification": self._extraer_valor(r"(Possible Attack|AS-[A-Z0-9\-]+)", alert_raw),
                "annotations": self._extraer_anotaciones(alert_raw)
            }
        except Exception as e:
            print(f"Error procesando alerta: {e}")
            return {"error": str(e), "raw_text": alert_raw[:200] + "..."}

    def _extraer_valor(self, pattern: str, text: str, default=None):
        match = re.search(pattern, text)
        return match.group(1) if match else default

    def _extraer_throughput(self, text: str) -> str:
        throughput_match = re.search(r"(\d{1,4}\.\d{1,2}\s?Mbps,\s?\d{1,4}\.\d{1,2}\s?Kpps)", text)
        if not throughput_match:
            throughput_match = re.search(r"(\d{1,4}\.\d{1,2}Mbps.*?)Kpps", text)
        return throughput_match.group(1).replace(" ", "") if throughput_match else None

    def _extraer_anotaciones(self, text: str) -> str:
        annotations_match = re.search(r"(The alert was generated.*?)\)", text, re.DOTALL)
        if annotations_match:
            return annotations_match.group(1).replace("\n", " ").strip() + ")"
        return "No annotations"