from typing import Dict, List
from informes.src.application.usecase.extraer_toptalkers import ExtraerTopTalkersUseCase
from informes.src.adapters.lector_pdf_pdfplumber import LectorPDFPdfPlumber
from informes.src.utils.generate_pdf_toptalkers import generar_pdf_toptalkers
from informes.src.utils.mongo_helpers import guardar_pdf_en_mongo

import base64
import os

class TopTalkersController:
    def __init__(self):
        lector = LectorPDFPdfPlumber()
        self.talkers_usecase = ExtraerTopTalkersUseCase(lector)

    def process_toptalkers_multiples(self, filepaths: List[str]) -> Dict:
        try:
            talkers = []
            for path in filepaths:
                talkers += self.talkers_usecase.ejecutar(path)

            print(f"Total de IPs combinadas: {len(talkers)}")

            pdf_path = generar_pdf_toptalkers(talkers)

            with open(pdf_path, "rb") as f:
                pdf_base64 = base64.b64encode(f.read()).decode('utf-8')
            guardar_pdf_en_mongo("toptalkers", os.path.basename(pdf_path), pdf_base64)

            os.remove(pdf_path)

            return {
                "files": filepaths,
                "status": "success",
                "toptalkers": talkers,
                "total_ips": len(talkers),
                "reporte_pdf": pdf_base64
            }

        except Exception as e:
            return {
                "files": filepaths,
                "status": "failed",
                "error": str(e),
                "suggestion": "Verifique que los PDFs contengan datos de top talkers con el formato correcto"
            }
