from src.cliente import Cliente
from src.exceptions import (
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    SoftwareFJError,
)
from src.logger_config import configurar_logger
from src.reserva import Reserva
from src.servicios import Servicio


class GestorSoftwareFJ:
    """Controlador principal que administra listas en memoria y el manejo de errores."""

    def __init__(self):
        self.logger = configurar_logger()
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []
        self.logger.info("Sistema Software FJ inicializado correctamente en memoria.")

    def registrar_cliente(self, documento: str, nombre: str, correo: str, telefono: str) -> Cliente | None:
        """Registra un cliente usando try/except/else para separar flujo normal y error."""
        try:
            if any(c.documento == str(documento).strip() for c in self.clientes):
                raise DatosInvalidosError(f"Ya existe un cliente registrado con documento {documento}.")
            nuevo_cliente = Cliente(documento, nombre, correo, telefono)
        except SoftwareFJError as err:
            self.logger.error(f"[{err.codigo_error}] Fallo al registrar cliente: {err}")
            return None
        else:
            self.clientes.append(nuevo_cliente)
            self.logger.info(f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    def registrar_servicio(self, servicio: Servicio) -> Servicio | None:
        """Agrega un servicio validado al catálogo usando try/except/finally."""
        operacion_exitosa = False
        try:
            if not isinstance(servicio, Servicio) or not servicio.validar_integridad():
                raise DatosInvalidosError("El objeto proporcionado no es un Servicio válido.")
            self.servicios.append(servicio)
            operacion_exitosa = True
            self.logger.info(f"Servicio agregado al catálogo: {servicio.obtener_resumen()}")
            return servicio
        except SoftwareFJError as err:
            self.logger.error(f"[{err.codigo_error}] Error registrando servicio: {err}")
            return None
        finally:
            estado = "EXITOSA" if operacion_exitosa else "FALLIDA"
            self.logger.debug(f"Auditoría registro de servicio finalizada (Estado: {estado}).")

    def crear_y_confirmar_reserva(
        self,
        cliente: Cliente | None,
        servicio: Servicio | None,
        duracion_horas: int,
        descuento: float = 0.0,
        recargo: float = 0.0,
    ) -> Reserva | None:
        """Crea y confirma una reserva aplicando encadenamiento de excepciones."""
        reserva = None
        try:
            reserva = Reserva(cliente, servicio, duracion_horas)
            reserva.confirmar(descuento=descuento, recargo=recargo)
        except SoftwareFJError as err:
            try:
                raise ReservaInvalidaError(
                    f"No se pudo completar la reserva solicitada: {err}"
                ) from err
            except ReservaInvalidaError as chained_err:
                self.logger.error(
                    f"[{chained_err.codigo_error}] {chained_err} | Causa raíz: {type(err).__name__}"
                )
            return None
        else:
            self.reservas.append(reserva)
            self.logger.info(f"Reserva confirmada: {reserva.obtener_resumen()}")
            return reserva
        finally:
            self.logger.debug(f"Total reservas activas en memoria: {len(self.reservas)}")

    def procesar_reserva(self, reserva: Reserva | None) -> None:
        """Procesa una reserva confirmada protegiendo la ejecución ante objetos nulos."""
        try:
            if reserva is None:
                raise OperacionNoPermitidaError("No se puede procesar una reserva inexistente (None).")
            mensaje = reserva.procesar()
        except SoftwareFJError as err:
            self.logger.error(f"[{err.codigo_error}] Error procesando reserva: {err}")
        else:
            self.logger.info(mensaje)

    def cancelar_reserva(self, reserva: Reserva | None, motivo: str = "Cancelación estándar") -> None:
        """Cancela una reserva gestionando cualquier transición no permitida."""
        try:
            if reserva is None:
                raise OperacionNoPermitidaError("No se puede cancelar una reserva inexistente (None).")
            reserva.cancelar(motivo)
        except SoftwareFJError as err:
            self.logger.error(f"[{err.codigo_error}] Error cancelando reserva: {err}")
        else:
            self.logger.warning(f"Reserva[{reserva.id}] CANCELADA. Motivo: {motivo}")