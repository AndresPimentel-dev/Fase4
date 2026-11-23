from abc import abstractmethod
from src.base import EntidadBase
from src.exceptions import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametroFaltanteError,
)


class Servicio(EntidadBase):
    """Clase abstracta que modela cualquier servicio ofrecido por Software FJ."""

    def __init__(self, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__()
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError(
                f"La tarifa base ({tarifa_base}) debe ser un número positivo mayor a cero."
            )
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros_servicio(self) -> bool:
        """Valida las reglas de negocio particulares de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Calcula el costo sin impuestos según la lógica polimórfica de cada subclase."""
        pass

    def calcular_costo_total(
        self,
        duracion_horas: int,
        impuesto_iva: float = 0.19,
        descuento_porcentaje: float = 0.0,
        recargo_urgencia: float = 0.0,
    ) -> float:
        """
        Método sobrecargado mediante parámetros opcionales para calcular costos
        con IVA, descuentos corporativos o recargos por urgencia.
        """
        try:
            if duracion_horas <= 0:
                raise DatosInvalidosError("La duración en horas debe ser mayor a 0.")
            if not (0 <= descuento_porcentaje <= 100):
                raise CalculoInconsistenteError(
                    f"Porcentaje de descuento fuera de rango (0-100): {descuento_porcentaje}"
                )
            if impuesto_iva < 0 or recargo_urgencia < 0:
                raise CalculoInconsistenteError("Impuestos o recargos no pueden ser negativos.")

            subtotal = self.calcular_costo_base(duracion_horas)
            valor_descuento = subtotal * (descuento_porcentaje / 100.0)
            base_gravable = subtotal - valor_descuento + recargo_urgencia
            total = round(base_gravable * (1 + impuesto_iva), 2)

            if total <= 0:
                raise CalculoInconsistenteError("El cálculo final arrojó un valor menor o igual a cero.")

            return total

        except (TypeError, ValueError) as err:
            raise CalculoInconsistenteError(
                f"Error aritmético calculando costo para '{self.nombre}': {err}"
            ) from err

    def validar_integridad(self) -> bool:
        return self._tarifa_base > 0 and self.validar_parametros_servicio()

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio[{self.id}] {self.nombre} | Tarifa: ${self.tarifa_base:,.2f}/h | {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas de reuniones o capacitación."""

    def __init__(self, nombre: str, tarifa_base: float, capacidad_personas: int, tiene_videobeam: bool = True):
        super().__init__(nombre, tarifa_base)
        self.capacidad_personas = capacidad_personas
        self.tiene_videobeam = tiene_videobeam
        self.validar_parametros_servicio()

    def validar_parametros_servicio(self) -> bool:
        if not isinstance(self.capacidad_personas, int) or self.capacidad_personas < 2:
            raise DatosInvalidosError("Una sala debe tener capacidad mínima para 2 personas.")
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        adicional_equipo = 15000.0 if self.tiene_videobeam else 0.0
        return (self.tarifa_base * duracion_horas) + adicional_equipo

    def obtener_resumen(self) -> str:
        return f"{super().obtener_resumen()} | Capacidad: {self.capacidad_personas} pers."


class AlquilerEquipo(Servicio):
    """Servicio especializado para préstamo de hardware (laptops, servidores, redes)."""

    def __init__(self, nombre: str, tarifa_base: float, categoria_equipo: str, deposito_garantia: float):
        super().__init__(nombre, tarifa_base)
        self.categoria_equipo = categoria_equipo
        self.deposito_garantia = deposito_garantia
        self.validar_parametros_servicio()

    def validar_parametros_servicio(self) -> bool:
        if not self.categoria_equipo or not self.categoria_equipo.strip():
            raise ParametroFaltanteError("Debe especificar la categoría del equipo.")
        if self.deposito_garantia < 0:
            raise DatosInvalidosError("El depósito de garantía no puede ser negativo.")
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        return (self.tarifa_base * duracion_horas) + self.deposito_garantia

    def obtener_resumen(self) -> str:
        return f"{super().obtener_resumen()} | Equipo: {self.categoria_equipo} (Garantía: ${self.deposito_garantia:,.2f})"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría de arquitectura de software o nube."""

    def __init__(self, nombre: str, tarifa_base: float, area_tecnica: str, nivel_seniority: str = "Senior"):
        super().__init__(nombre, tarifa_base)
        self.area_tecnica = area_tecnica
        self.nivel_seniority = nivel_seniority
        self.validar_parametros_servicio()

    def validar_parametros_servicio(self) -> bool:
        niveles_validos = {"Junior", "Mid", "Senior", "Arquitecto"}
        if self.nivel_seniority not in niveles_validos:
            raise DatosInvalidosError(
                f"Nivel '{self.nivel_seniority}' inválido. Use: {', '.join(niveles_validos)}."
            )
        if not self.area_tecnica or not self.area_tecnica.strip():
            raise ParametroFaltanteError("El área técnica de la asesoría es obligatoria.")
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        multiplicadores = {"Junior": 1.0, "Mid": 1.25, "Senior": 1.5, "Arquitecto": 2.0}
        factor = multiplicadores[self.nivel_seniority]
        return self.tarifa_base * duracion_horas * factor

    def obtener_resumen(self) -> str:
        return f"{super().obtener_resumen()} | Área: {self.area_tecnica} ({self.nivel_seniority})"