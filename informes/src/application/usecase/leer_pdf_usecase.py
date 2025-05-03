from informes.src.Domain.interface.lector_pdf_interface import LectorPDFInterface
class LeerPDFUseCase:
    def __init__(self, lector_pdf: LectorPDFInterface):
        self.lector_pdf = lector_pdf

    def ejecutar(self, ruta_pdf: str) -> str:
        return self.lector_pdf.leer(ruta_pdf)