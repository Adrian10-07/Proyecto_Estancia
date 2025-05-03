from typing import Dict, List
from informes.src.application.usecase.extraer_aplicaciones_usecase import ExtraerAplicacionesUseCase
from informes.src.adapters.lector_pdf_pdfplumber import LectorPDFPdfPlumber
from informes.src.utils.generate_pdf_aplicaciones import generar_pdf_aplicaciones
from informes.src.utils.mongo_helpers import guardar_pdf_en_mongo
import base64
import os

class AplicacionesController:
    def __init__(self):
        lector = LectorPDFPdfPlumber()
        self.aplicaciones_usecase = ExtraerAplicacionesUseCase(lector)

    def process_aplicaciones_multiples(self, filepaths: List[str]) -> Dict:
        try:
            aplicaciones = []
            for path in filepaths:
                aplicaciones += self.aplicaciones_usecase.ejecutar(path)

            print(f"Total de aplicaciones combinadas: {len(aplicaciones)}")

            pdf_path = generar_pdf_aplicaciones(aplicaciones)

            with open(pdf_path, "rb") as f:
                pdf_base64 = base64.b64encode(f.read()).decode('utf-8')
                
            guardar_pdf_en_mongo("aplicaciones", os.path.basename(pdf_path), pdf_base64)

            os.remove(pdf_path)

            return {
                "files": filepaths,
                "status": "success",
                "aplicaciones": aplicaciones,
                "total_aplicaciones": len(aplicaciones),
                "reporte_pdf": pdf_base64
            }

        except Exception as e:
            return {
                "files": filepaths,
                "status": "failed",
                "error": str(e),
                "suggestion": "Verifique que los PDFs tengan el formato correcto de reporte de aplicaciones"
            }
