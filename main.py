from src.exceptions import SoftwareFJError
from src.gestor import GestorSoftwareFJ
from src.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def ejecutar_simulaciones():
    """Ejecuta 12 operaciones completas (válidas e inválidas) demostrando estabilidad total."""
    sistema = GestorSoftwareFJ()
    print("\n=== INICIANDO SIMULACIÓN DE OPERACIONES - SOFTWARE FJ ===\n")

    # 1. Registro VÁLIDO de cliente 1
    c1 = sistema.registrar_cliente("1020304050", "Andrés Pimentel", "andres@softwarefj.com", "3001234567")

    # 2. Registro VÁLIDO de cliente 2
    c2 = sistema.registrar_cliente("987654321", "Laura Gómez", "laura.gomez@empresa.co", "3109876543")

    # 3. Registro INVÁLIDO de cliente (correo mal formado y documento corto)
    sistema.registrar_cliente("123", "Carlos Error", "correo_sin_arroba", "3001112233")

    # 4. Registro INVÁLIDO de cliente (documento duplicado)
    sistema.registrar_cliente("1020304050", "Andrés Duplicado", "otro@correo.com", "3005556677")

    # 5. Creación VÁLIDA de 3 servicios especializados (Polimorfismo)
    sala_juntas = sistema.registrar_servicio(
        ReservaSala("Sala Innovación A", tarifa_base=80000, capacidad_personas=10, tiene_videobeam=True)
    )
    servidor_gpu = sistema.registrar_servicio(
        AlquilerEquipo("Servidor Dell PowerEdge", tarifa_base=50000, categoria_equipo="Servidores", deposito_garantia=100000)
    )
    asesoria_cloud = sistema.registrar_servicio(
        AsesoriaEspecializada("Arquitectura AWS & Docker", tarifa_base=120000, area_tecnica="Cloud & DevOps", nivel_seniority="Arquitecto")
    )

    # 6. Creación INVÁLIDA de servicio (tarifa negativa capturada antes de registrar)
    try:
        servicio_malo = ReservaSala("Sala Inválida", tarifa_base=-5000, capacidad_personas=4)
        sistema.registrar_servicio(servicio_malo)
    except SoftwareFJError as err:
        sistema.logger.error(f"[{err.codigo_error}] Instanciación directa bloqueada: {err}")

    # 7. Reserva EXITOSA 1 (Sala con descuento corporativo del 10%)
    res1 = sistema.crear_y_confirmar_reserva(c1, sala_juntas, duracion_horas=4, descuento=10.0)

    # 8. Reserva FALLIDA 2 (Intento de reservar la misma sala que ya quedó ocupada)
    sistema.crear_y_confirmar_reserva(c2, sala_juntas, duracion_horas=2)

    # 9. Reserva FALLIDA 3 (Duración negativa y descuento fuera de rango)
    sistema.crear_y_confirmar_reserva(c2, servidor_gpu, duracion_horas=-3)
    sistema.crear_y_confirmar_reserva(c2, servidor_gpu, duracion_horas=5, descuento=150.0)

    # 10. Procesamiento EXITOSO de la Reserva 1 (libera la sala automáticamente)
    sistema.procesar_reserva(res1)

    # 11. Intento INVÁLIDO de cancelar una reserva que ya fue PROCESADA
    sistema.cancelar_reserva(res1, motivo="Intento tardío de cancelación")

    # 12. Reserva EXITOSA 4 y posterior CANCELACIÓN VÁLIDA (Asesoría con recargo por urgencia)
    res4 = sistema.crear_y_confirmar_reserva(c2, asesoria_cloud, duracion_horas=3, recargo=50000.0)
    sistema.cancelar_reserva(res4, motivo="Reprogramación de sprint del cliente")

    print("\n=== RESUMEN FINAL DEL SISTEMA (SIN INTERRUPCIONES) ===")
    print(f"Clientes activos: {len(sistema.clientes)}")
    print(f"Servicios en catálogo: {len(sistema.servicios)}")
    print(f"Reservas registradas: {len(sistema.reservas)}")
    print("Revisa el archivo 'logs/sistema_fj.log' para ver la traza completa de eventos y errores.\n")


if __name__ == "__main__":
    ejecutar_simulaciones()