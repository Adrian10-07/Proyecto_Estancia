import pdfplumber
from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface

class LectorPDFPdfPlumber(LectorPDFInterface):
    def leer(self, ruta_pdf: str) -> str:
        texto = ""
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""
        return texto 