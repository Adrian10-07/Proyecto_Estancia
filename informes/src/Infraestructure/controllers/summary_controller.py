from typing import List, Dict
from informes.src.application.usecase.extraer_summary_usecase import ExtraerSummaryUseCase
from informes.src.adapters.lector_pdf_pdfplumber import LectorPDFPdfPlumber
from informes.src.utils.generate_pdf_summary import generar_pdf_summary
from informes.src.utils.mongo_helpers import guardar_pdf_en_mongo
import base64
import os

class SummaryController:
    def __init__(self):
        lector = LectorPDFPdfPlumber()
        self.summary_usecase = ExtraerSummaryUseCase(lector)

    def process_summary_multiples(self, filepaths: List[str]) -> Dict:
        try:
            resumenes = []
            for path in filepaths:
                resumen = self.summary_usecase.ejecutar(path)
                if resumen:
                    resumenes.append(resumen)

            if not resumenes:
                raise ValueError("No se extrajo ningún resumen válido de los archivos.")

            pdf_path = generar_pdf_summary(resumenes)

            with open(pdf_path, "rb") as f:
                pdf_base64 = base64.b64encode(f.read()).decode('utf-8')
            guardar_pdf_en_mongo("summary", os.path.basename(pdf_path), pdf_base64)

            os.remove(pdf_path)

            return {
                "files": filepaths,
                "status": "success",
                "resumenes": resumenes,
                "total_resumenes": len(resumenes),
                "reporte_pdf": pdf_base64
            }

        except Exception as e:
            return {
                "files": filepaths,
                "status": "failed",
                "error": str(e),
                "suggestion": "Verifique que los PDFs contengan métricas con el formato esperado"
            }
