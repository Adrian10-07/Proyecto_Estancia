from abc import ABC, abstractmethod

class LectorPDFInterface(ABC):
    @abstractmethod
    def leer(self, ruta_pdf: str) -> str:
        pass
