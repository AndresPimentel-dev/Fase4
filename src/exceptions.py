class SoftwareFJError(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR-000"):
        super().__init__(mensaje)
        self.codigo_error = codigo_error


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos ingresados no cumplen el formato o tipo esperado."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-DATOS")


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un argumento obligatorio para crear una entidad."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-PARAM")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin cupo."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-SERV-DISP")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva presenta conflictos de estado o duración."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-RESV")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando ocurre un fallo aritmético o valores negativos en costos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-CALC")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza al intentar transiciones de estado prohibidas en el negocio."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-OPER")