from src.base import EntidadBase
from src.cliente import Cliente
from src.exceptions import (
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from src.servicios import Servicio


class Reserva(EntidadBase):
    """Integra un Cliente y un Servicio, gestionando su ciclo de vida y costos."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere una instancia válida de Servicio.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ReservaInvalidaError(
                f"Duración inválida ({duracion_horas}h): debe ser un entero positivo."
            )
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible actualmente."
            )

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "PENDIENTE"
        self._costo_final = 0.0

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion_horas(self) -> int:
        return self._duracion_horas

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_final(self) -> float:
        return self._costo_final

    def confirmar(self, descuento: float = 0.0, recargo: float = 0.0) -> None:
        """Confirma la reserva, calcula el costo total y bloquea el servicio."""
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado '{self._estado}'."
            )
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' fue ocupado antes de confirmar."
            )

        self._costo_final = self._servicio.calcular_costo_total(
            duracion_horas=self._duracion_horas,
            descuento_porcentaje=descuento,
            recargo_urgencia=recargo,
        )
        self._estado = "CONFIRMADA"
        self._servicio.disponible = False

    def procesar(self) -> str:
        """Ejecuta el servicio de una reserva previamente confirmada."""
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: '{self._estado}')."
            )
        self._estado = "PROCESADA"
        self._servicio.disponible = True
        return f"Reserva {self.id} ejecutada con éxito. Total facturado: ${self._costo_final:,.2f}"

    def cancelar(self, motivo: str = "Solicitud del cliente") -> None:
        """Cancela una reserva pendiente o confirmada y libera el servicio."""
        if self._estado in ("PROCESADA", "CANCELADA"):
            raise OperacionNoPermitidaError(
                f"Imposible cancelar una reserva en estado '{self._estado}'."
            )
        if self._estado == "CONFIRMADA":
            self._servicio.disponible = True
        self._estado = "CANCELADA"

    def validar_integridad(self) -> bool:
        return self._estado in self.ESTADOS_VALIDOS and self._duracion_horas > 0

    def obtener_resumen(self) -> str:
        return (
            f"Reserva[{self.id}] Estado: {self.estado} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} ({self.duracion_horas}h) | Total: ${self.costo_final:,.2f}"
        )