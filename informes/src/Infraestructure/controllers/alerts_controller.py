from typing import List
from informes.src.application.usecase.extraer_alertas_usecase import ExtraerAlertasUseCase
from informes.src.adapters.lector_pdf_pdfplumber import LectorPDFPdfPlumber
from informes.src.utils.generate_pdf_alerts import generar_reporte_pdf
from informes.src.utils.mongo_helpers import guardar_pdf_en_mongo

import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
import base64
import pandas as pd


class AlertasController:
    def __init__(self):
        lector = LectorPDFPdfPlumber()
        self.alertas_usecase = ExtraerAlertasUseCase(lector)

    def process_alertas_multiples(self, filepaths: List[str]) -> dict:
        try:
            alertas = []
            for path in filepaths:
                alertas += self.alertas_usecase.ejecutar(path)

            print(f"Total de alertas combinadas: {len(alertas)}")

            # Crear gráfico en base64
            plt.figure(figsize=(8, 5))
            sns.countplot(data=pd.DataFrame(alertas), x='importance', order=['Low', 'Medium', 'High'])
            plt.title('Cantidad de Alertas por Importancia')
            plt.tight_layout()

            img_stream = io.BytesIO()
            plt.savefig(img_stream, format='png')
            img_stream.seek(0)
            graph_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
            plt.close()

            # Generar el reporte PDF
            pdf_path = generar_reporte_pdf(alertas)

            with open(pdf_path, "rb") as f:
                pdf_base64 = base64.b64encode(f.read()).decode('utf-8')

            # Guardar en MongoDB
            guardar_pdf_en_mongo("alertas", os.path.basename(pdf_path), pdf_base64)

            os.remove(pdf_path)

            return {
                "files": filepaths,
                "status": "success",
                "alertas": alertas,
                "total_alertas": len(alertas),
                "reporte_pdf": pdf_base64,
                "grafico_base64": graph_base64
            }

        except Exception as e:
            return {
                "files": filepaths,
                "status": "failed",
                "error": str(e)
            }
