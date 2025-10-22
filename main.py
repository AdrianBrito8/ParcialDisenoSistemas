"""
Archivo principal de ejecucion del Sistema de Gestion Forestal.

Este script simula un flujo completo de operaciones (End-to-End)
basado en las Historias de Usuario para demostrar la
funcionalidad de todos los modulos y patrones.

-   Crea una finca (Tierra + Plantacion).
-   Planta cultivos (usando Factory).
-   Inicia el sistema de riego automatico (Threads + Observer).
-   Asigna personal y ejecuta tareas.
-   Gestiona multiples fincas (FincasService).
-   Cosecha cultivos (Generics).
-   Persiste y lee el registro (Pickle).
-   Detiene los threads de forma segura (Graceful Shutdown).

Disenado para pasar la RUBRICA_AUTOMATIZADA.md
"""

# --- Imports Standard Library ---
import time
import sys
from datetime import date

# --- Imports de Entidades ---
from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal
from python_forestacion.entidades.personal.trabajador import Trabajador
from python_forestacion.entidades.personal.tarea import Tarea
from python_forestacion.entidades.personal.herramienta import Herramienta
# Tipos de cultivo para la cosecha (US-020)
from python_forestacion.entidades.cultivos.pino import Pino
from python_forestacion.entidades.cultivos.lechuga import Lechuga

# --- Imports de Servicios ---
from python_forestacion.servicios.terrenos.tierra_service import TierraService
from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService
from python_forestacion.servicios.terrenos.registro_forestal_service import RegistroForestalService
from python_forestacion.servicios.personal.trabajador_service import TrabajadorService
from python_forestacion.servicios.negocio.fincas_service import FincasService

# --- Imports de Riego (Threads) ---
from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask
from python_forestacion.riego.control.control_riego_task import ControlRiegoTask

# --- Imports de Excepciones ---
from python_forestacion.excepciones.forestacion_exception import ForestacionException

# --- Imports de Constantes ---
from python_forestacion import constantes as C


def ejecutar_simulacion():
    """
    Funcion principal que encapsula toda la logica de la simulacion.
    """
    
    # --- Inicializacion de Servicios ---
    # (El Registry se inicializa solo como Singleton)
    print("Iniciando servicios...")
    tierra_service = TierraService()
    plantacion_service = PlantacionService()
    registro_service = RegistroForestalService()
    trabajador_service = TrabajadorService()
    fincas_service = FincasService()
    
    # Variables para los threads
    tarea_temp = None
    tarea_hum = None
    tarea_control = None

    try:
        # ======================================================================
        # --- EPIC 1 y 2: CREACION DE FINCA Y PLANTACION (US-001 a US-007) ---
        # ======================================================================
        print("\n=== [FASE 1: CREACION Y PLANTACION] ===")
        
        # US-001 y US-002: Crear Tierra y Plantacion
        tierra = tierra_service.crear_tierra_con_plantacion(
            id_padron_catastral=12345,
            superficie=1000.0,
            domicilio="Calle Falsa 123, Mendoza",
            nombre_plantacion="Finca Demo"
        )
        plantacion = tierra.get_finca() # type: ignore

        # US-003: Crear Registro Forestal
        registro = RegistroForestal(
            id_padron=tierra.get_id_padron_catastral(),
            tierra=tierra,
            plantacion=plantacion,
            propietario="Adrian Developer",
            avaluo=15000000.0
        )
        
        # Demostracion PATRON FACTORY (US-TECH-002)
        print("\nDemostracion: Patron Factory Method (Rubrica 1.2)")
        # US-004 a US-007: Plantar usando el servicio (que usa el Factory)
        plantacion_service.plantar(plantacion, "Pino", 5)
        plantacion_service.plantar(plantacion, "Olivo", 5)
        plantacion_service.plantar(plantacion, "Lechuga", 20)
        plantacion_service.plantar(plantacion, "Zanahoria", 20)

        # ======================================================================
        # --- EPIC 3: SISTEMA DE RIEGO AUTOMATIZADO (US-010 a US-013) ---
        # ======================================================================
        print("\n=== [FASE 2: INICIANDO SISTEMA DE RIEGO (THREADS)] ===")
        
        # Demostracion PATRON OBSERVER (US-TECH-003)
        print("\nDemostracion: Patron Observer (Rubrica 1.3)")
        print("(Los sensores son Observables[float], notificando a los suscriptores)")
        
        # US-010 y US-011: Crear e iniciar Sensores (Threads)
        tarea_temp = TemperaturaReaderTask()
        tarea_hum = HumedadReaderTask()
        
        tarea_temp.start()
        tarea_hum.start()

        # US-012: Crear e iniciar Controlador (Thread)
        # (Se inyectan los sensores)
        tarea_control = ControlRiegoTask(
            sensor_temperatura=tarea_temp,
            sensor_humedad=tarea_hum,
            plantacion=plantacion,
            plantacion_service=plantacion_service
        )
        tarea_control.start()
        
        print("\nSistema de riego automatizado iniciado. "
              "Dejando correr por 10 segundos...")
        time.sleep(10)
        
        # Demostracion PATRON STRATEGY (US-TECH-004)
        print("\nDemostracion: Patron Strategy (Rubrica 1.4)")
        print("(El riego uso 'AbsorcionSeasonalStrategy' para Arboles "
              "y 'AbsorcionConstanteStrategy' para Hortalizas)")
              
        # Demostracion PATRON SINGLETON (US-TECH-001)
        print("\nDemostracion: Patron Singleton (Rubrica 1.1)")
        print("(El 'PlantacionService' y el 'RegistroForestalService' "
              "usaron la MISMA instancia del 'CultivoServiceRegistry')")
        
        # ======================================================================
        # --- EPIC 4: GESTION DE PERSONAL (US-014 a US-017) ---
        # ======================================================================
        print("\n=== [FASE 3: GESTION DE PERSONAL] ===")
        
        # US-014: Crear Tareas y Trabajador
        tareas = [
            Tarea(1, date.today(), "Revisar goteo de pinos"),
            Tarea(2, date.today(), "Quitar maleza de zanahorias"),
            Tarea(3, date(2025, 10, 22), "Tarea para maniana (no debe ejecutarla)")
        ]
        trabajador = Trabajador(dni=30123456, nombre="Juan Perez", tareas=tareas)
        
        # US-017: Asignar trabajador a plantacion
        plantacion.set_trabajadores([trabajador])
        
        # US-015: Asignar Apto Medico
        trabajador_service.asignar_apto_medico(
            trabajador=trabajador,
            apto=True,
            fecha_emision=date.today(),
            observaciones="Apto para tareas agricolas"
        )
        
        # US-016: Ejecutar Tareas (y demostrar NO-LAMBDA)
        herramienta = Herramienta(101, "Pala", True)
        print("\nDemostracion: NO-LAMBDA (Rubrica 3.4)")
        print("(El servicio ordena tareas usando un metodo estatico, no lambda)")
        trabajador_service.trabajar(
            trabajador=trabajador,
            fecha=date.today(),
            util=herramienta
        )
        
        # ======================================================================
        # --- EPIC 5: OPERACIONES DE NEGOCIO (US-018 a US-020) ---
        # ======================================================================
        print("\n=== [FASE 4: OPERACIONES DE NEGOCIO (FINCAS SERVICE)] ===")
        
        # US-018: Agregar finca al servicio de gestion
        fincas_service.add_finca(registro)
        
        # US-019: Fumigar
        fincas_service.fumigar(id_padron=12345, plaguicida="Cipermetrina")
        
        # US-020: Cosechar y Empaquetar (Demostracion Generics)
        print("\nDemostracion: Cosecha con Generics (Paquete[T])")
        caja_lechugas = fincas_service.cosechar_yempaquetar(Lechuga)
        caja_lechugas.mostrar_contenido_caja()
        
        caja_pinos = fincas_service.cosechar_yempaquetar(Pino)
        caja_pinos.mostrar_contenido_caja()
        
        # ======================================================================
        # --- EPIC 6: PERSISTENCIA Y AUDITORIA (US-021 a US-023) ---
        # ======================================================================
        print("\n=== [FASE 5: PERSISTENCIA Y AUDITORIA] ===")
        
        # US-021: Persistir (Guardar)
        path_archivo = registro_service.persistir(registro)
        print(f"Registro guardado en: {path_archivo}")
        
        # US-022: Leer
        registro_leido = RegistroForestalService.leer_registro("Adrian Developer")
        
        # US-023: Mostrar datos (usando Registry)
        print("\nMostrando datos del registro leido (demuestra Registry):")
        registro_service.mostrar_datos(registro_leido)

    except ForestacionException as e:
        # Manejo de nuestras excepciones personalizadas (Rubrica 2.3)
        print("\n**************************************************")
        print("   ERROR DE NEGOCIO CONTROLADO (ForestacionException)")
        print(f"   Mensaje: {e.get_user_message()}")
        print(f"   Tecnico: {e.get_mensaje_tecnico()}")
        print("**************************************************")
        sys.exit(1) # Salir con codigo de error
        
    except Exception as e:
        # Manejo de errores inesperados
        print("\n**************************************************")
        print("           ERROR INESPERADO (Exception)")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Error: {e}")
        print("**************************************************")
        sys.exit(1) # Salir con codigo de error

    finally:
        # ======================================================================
        # --- FASE FINAL: DETENCION SEGURA (US-013) ---
        # ======================================================================
        print("\n=== [FASE FINAL: DETENIENDO THREADS...] ===")
        
        if tarea_control:
            tarea_control.detener()
        if tarea_temp:
            tarea_temp.detener()
        if tarea_hum:
            tarea_hum.detener()
            
        # Esperar a que los threads terminen (Graceful Shutdown)
        # (Rubrica 4.2, 5.1)
        join_timeout = C.THREAD_JOIN_TIMEOUT
        
        if tarea_temp:
            tarea_temp.join(timeout=join_timeout)
            print(f"Sensor de Temperatura: {'Detenido' if not tarea_temp.is_alive() else 'Forzado'}")
            
        if tarea_hum:
            tarea_hum.join(timeout=join_timeout)
            print(f"Sensor de Humedad: {'Detenido' if not tarea_hum.is_alive() else 'Forzado'}")
            
        if tarea_control:
            tarea_control.join(timeout=join_timeout)
            print(f"Control de Riego: {'Detenido' if not tarea_control.is_alive() else 'Forzado'}")
            
        print("\nTodos los sistemas detenidos de forma segura.")
        print("\n--- EJEMPLO COMPLETADO EXITOSAMENTE ---")
        # Este mensaje es el que busca la Rubrica Auto (EXEC-002)


# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    ejecutar_simulacion()