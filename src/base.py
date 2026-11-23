from abc import ABC, abstractmethod
from datetime import datetime
import uuid


class EntidadBase(ABC):
    """Clase abstracta raíz que define identidad y auditoría para las entidades."""

    def __init__(self, id_entidad: str | None = None):
        self._id = id_entidad if id_entidad else str(uuid.uuid4())[:8].upper()
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        """Retorna el identificador único de la entidad (solo lectura)."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora de creación de la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Método abstracto que obliga a las subclases a validar su estado interno."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto para representar la entidad de forma legible."""
        pass