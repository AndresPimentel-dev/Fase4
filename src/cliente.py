import re
from src.base import EntidadBase
from src.exceptions import DatosInvalidosError, ParametroFaltanteError


class Cliente(EntidadBase):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, documento: str, nombre: str, correo: str, telefono: str):
        super().__init__()
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self._activo = True
        self.validar_integridad()

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")
        if not str(valor).isdigit() or len(str(valor)) < 6:
            raise DatosInvalidosError(
                f"Documento inválido '{valor}': debe ser numérico y tener al menos 6 dígitos."
            )
        self._documento = str(valor).strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre debe contener al menos 3 caracteres.")
        self._nombre = valor.strip().title()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or not valor.strip():
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, valor.strip()):
            raise DatosInvalidosError(f"Formato de correo inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not str(valor).strip().isdigit() or len(str(valor).strip()) < 7:
            raise DatosInvalidosError(
                f"Teléfono inválido '{valor}': debe contener al menos 7 dígitos numéricos."
            )
        self._telefono = str(valor).strip()

    @property
    def activo(self) -> bool:
        return self._activo

    def validar_integridad(self) -> bool:
        """Verifica que todos los campos encapsulados mantengan consistencia."""
        return all([self._documento, self._nombre, self._correo, self._telefono])

    def obtener_resumen(self) -> str:
        return f"Cliente[{self.id}] {self.nombre} (Doc: {self.documento} | Email: {self.correo})"