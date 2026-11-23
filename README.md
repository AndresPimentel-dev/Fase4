# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para la **Fase 4 – Prácticas simuladas** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripción Técnica
Aplicación orientada a objetos en Python sin uso de bases de datos (persistencia en memoria mediante colecciones y auditoría en archivos `.log`). Implementa:
- **Abstracción y Herencia:** Clases abstractas `EntidadBase` y `Servicio` con especializaciones (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`).
- **Encapsulación:** Validación estricta de atributos mediante `@property` y *setters* en `Cliente`, `Servicio` y `Reserva`.
- **Polimorfismo y Sobrecarga:** Cálculo dinámico de tarifas base por tipo de servicio y sobrecarga mediante parámetros opcionales (IVA, descuentos y recargos).
- **Manejo Avanzado de Excepciones:** Jerarquía de excepciones personalizadas (`SoftwareFJError`), bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones (`raise ... from err`).

## Ejecución
```bash
python main.py