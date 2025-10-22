"""
Modulo del servicio RegistroForestalService.
Maneja la logica de persistencia (guardar/leer) y
la visualizacion de datos completos del registro.
"""

# --- Imports Standard Library ---
import os
import pickle
from typing import TYPE_CHECKING

# --- Imports de Constantes ---
from python_forestacion import constantes as C

# --- Imports de Patrones ---
# 1. Importa el Registry (Singleton) para mostrar datos de cultivos
from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry

# --- Imports de Excepciones ---
from python_forestacion.excepciones.persistencia_exception import PersistenciaException, TipoOperacion
from python_forestacion.excepciones import mensajes_exception as MSG

# --- Imports de Entidades ---
if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal


class RegistroForestalService:
    """
    Servicio para gestionar la logica de negocio de los Registros Forestales.
    
    Implementa US-021 (Persistir), US-022 (Leer) y US-023 (Mostrar).
    """

    def __init__(self):
        """
        Inicializa el RegistroForestalService.
        
        Obtiene la instancia unica (Singleton) del Registry.
        """
        self._registry = CultivoServiceRegistry.get_instance()

    def mostrar_datos(self, registro: RegistroForestal) -> None:
        """
        Muestra un reporte completo del registro forestal.
        Implementacion de US-023.
        
        Usa el Registry para despachar polimorficamente
        la visualizacion de cada cultivo (US-009).

        Args:
            registro (RegistroForestal): El registro a mostrar.
        """
        plantacion = registro.get_plantacion()
        tierra = registro.get_tierra()
        cultivos = plantacion.get_cultivos()

        print("\n=================================")
        print("     REGISTRO FORESTAL     ")
        print("=================================")
        print(f"Padron:      {registro.get_id_padron()}")
        print(f"Propietario: {registro.get_propietario()}")
        print(f"Avaluo:      ${registro.get_avaluo():,.2f}")
        print(f"Domicilio:   {tierra.get_domicilio()}")
        print(f"Superficie:  {tierra.get_superficie()} m²")
        print(f"Plantados:   {len(cultivos)} cultivos")
        print("____________________________")
        print("Listado de Cultivos plantados:")
        
        if not cultivos:
            print("(No hay cultivos en la plantacion)")
        else:
            for cultivo in cultivos:
                print("---")
                # Llama al Registry (Singleton) para que el
                # servicio correcto (PinoService, etc.) muestre los datos.
                self._registry.mostrar_datos(cultivo)
        
        print("=================================\n")

    def persistir(self, registro: RegistroForestal) -> str:
        """
        Guarda (serializa) un RegistroForestal en disco usando Pickle.
        Implementacion de US-021.

        Args:
            registro (RegistroForestal): El objeto a persistir.

        Raises:
            PersistenciaException: Si ocurre un error de IO o Pickle.
            ValueError: Si el propietario es nulo o vacio.

        Returns:
            str: El path completo del archivo guardado.
        """
        propietario = registro.get_propietario()
        if not propietario:
            raise ValueError("El propietario no puede ser nulo o vacio")

        # 1. Asegurar que el directorio 'data/' exista
        directorio = C.DIRECTORIO_DATA
        os.makedirs(directorio, exist_ok=True)

        # 2. Construir el path del archivo
        nombre_archivo = f"{propietario}{C.EXTENSION_DATA}"
        path_completo = os.path.join(directorio, nombre_archivo)
        
        print(f"\n--- Intentando persistir registro en {path_completo} ---")

        # 3. Escribir el archivo
        try:
            with open(path_completo, 'wb') as f:
                pickle.dump(registro, f)
                
            print(f"Registro de {propietario} persistido exitosamente.")
            return path_completo
            
        except (IOError, OSError) as e:
            raise PersistenciaException(
                mensaje_tecnico=MSG.TEC_ESCRIBIR_IO.format(directorio) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_ESCRIBIR_IO,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.ESCRIBIR
            )
        except pickle.PickleError as e:
            raise PersistenciaException(
                mensaje_tecnico=MSG.TEC_ESCRIBIR_PICKLE.format(propietario) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_ESCRIBIR_PICKLE,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.ESCRIBIR
            )
        except Exception as e:
            raise PersistenciaException(
                mensaje_tecnico=MSG.TEC_ESCRIBIR_OTRO.format(path_completo) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_ESCRIBIR_OTRO,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.ESCRIBIR
            )

    @staticmethod
    def leer_registro(propietario: str) -> RegistroForestal:
        """
        Carga (deserializa) un RegistroForestal desde disco.
        Implementacion de US-022.
        
        Es un metodo estatico porque no necesita estado (self).

        Args:
            propietario (str): El nombre del propietario (usado para el nombre del archivo).

        Raises:
            PersistenciaException: Si el archivo no existe o esta corrupto.
            ValueError: Si el propietario es nulo o vacio.

        Returns:
            RegistroForestal: El objeto recuperado.
        """
        if not propietario:
            raise ValueError("El nombre del propietario no puede ser nulo o vacio")

        # 1. Construir el path del archivo
        nombre_archivo = f"{propietario}{C.EXTENSION_DATA}"
        path_completo = os.path.join(C.DIRECTORIO_DATA, nombre_archivo)
        
        print(f"\n--- Intentando leer registro desde {path_completo} ---")

        # 2. Validar que el archivo exista
        if not os.path.exists(path_completo):
            raise PersistenciaException(
                mensaje_tecnico=MSG.TEC_LEER_NO_EXISTE.format(path_completo),
                mensaje_usuario=MSG.USR_LEER_NO_EXISTE,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.LEER
            )

        # 3. Leer el archivo
        try:
            with open(path_completo, 'rb') as f:
                registro_leido = pickle.load(f)
                
            print(f"Registro de {propietario} recuperado exitosamente.")
            return registro_leido
            
        except (pickle.UnpicklingError, EOFError, ImportError, IndexError) as e:
            # Errores comunes de un archivo pickle corrupto o vacio
            raise PersistenciaException(
                mensaje_tecnico=MSG.TEC_LEER_CORRUPTO.format(path_completo) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_LEER_CORRUPTO,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.LEER
            )
        except Exception as e:
            raise PersistenciaException(
                mensaje_tecnico=MSG.TEC_LEER_OTRO.format(path_completo) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_LEER_OTRO,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.LEER
            )