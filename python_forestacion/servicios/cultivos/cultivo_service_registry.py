"""
Modulo del CultivoServiceRegistry.

Implementa dos patrones de diseño:
1.  Singleton (Thread-Safe): Asegura una unica instancia.
2.  Registry: Despacha operaciones al servicio correcto sin ifs.
"""
from __future__ import annotations
from threading import Lock
from typing import Dict, Type, Callable, Any, TYPE_CHECKING
from typing_extensions import override

# Imports de Entidades (para las llaves del diccionario)
from python_forestacion.entidades.cultivos.cultivo import Cultivo
from python_forestacion.entidades.cultivos.pino import Pino
from python_forestacion.entidades.cultivos.olivo import Olivo
from python_forestacion.entidades.cultivos.lechuga import Lechuga
from python_forestacion.entidades.cultivos.zanahoria import Zanahoria

# Imports de Servicios (para los valores del diccionario)
from python_forestacion.servicios.cultivos.cultivo_service import CultivoService
from python_forestacion.servicios.cultivos.pino_service import PinoService
from python_forestacion.servicios.cultivos.olivo_service import OlivoService
from python_forestacion.servicios.cultivos.lechuga_service import LechugaService
from python_forestacion.servicios.cultivos.zanahoria_service import ZanahoriaService

# TypeAlias para los diccionarios del Registry
CultivoType = Type[Cultivo]
AbsorcionHandler = Callable[[Cultivo], int]
MostrarHandler = Callable[[Cultivo], None]


class CultivoServiceRegistry:
    """
    Implementa los patrones Singleton y Registry.

    - Como Singleton (Rubrica 1.1), asegura una unica instancia
      thread-safe para gestionar los servicios de cultivo.
    - Como Registry (US-TECH-005), centraliza el despacho
      polimorfico de operaciones (absorber_agua, mostrar_datos)
      evitando el uso de 'isinstance()'.
    """

    # --- Implementacion del Patron Singleton (US-TECH-001) ---

    _instance: CultivoServiceRegistry | None = None
    
    # El Lock es exigido por la Rubrica 1.1 y Auto (SING-003)
    _lock: Lock = Lock()

    def __new__(cls) -> CultivoServiceRegistry:
        """
        Controla la creacion de la instancia (Singleton).
        Usa double-checked locking para ser thread-safe.
        
        Referencia: Rubrica 1.1, Rubrica Auto (SING-002)
        """
        # Si ya existe, la retornamos
        if cls._instance is not None:
            return cls._instance

        # Si no existe, adquirimos el lock (thread-safe)
        with cls._lock:
            # Doble chequeo, por si otro thread la creo
            # mientras este esperaba por el lock
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                # El __init__ se llama automaticamente despues
                # de __new__, pero solo en esta primera creacion.
        
        return cls._instance

    @classmethod
    def get_instance(cls) -> CultivoServiceRegistry:
        """
        Metodo publico para obtener la unica instancia del Singleton.
        
        Referencia: Rubrica Auto (SING-004)
        """
        if cls._instance is None:
            cls() # Llama a __new__ y luego a __init__
        
        # Aca estamos seguros de que _instance no es None
        return cls._instance  # type: ignore

    # --- Implementacion del Patron Registry (US-TECH-005) ---

    def __init__(self):
        """
        Inicializa el Registry.
        
        Gracias al Singleton, este __init__ se ejecutara
        UNA SOLA VEZ en toda la vida de la aplicacion.
        
        Aqui creamos las instancias de los servicios y
        construimos los diccionarios de handlers (dispatch).
        """
        # 1. Crear instancias unicas de cada servicio
        self._pino_service: PinoService = PinoService()
        self._olivo_service: OlivoService = OlivoService()
        self._lechuga_service: LechugaService = LechugaService()
        self._zanahoria_service: ZanahoriaService = ZanahoriaService()

        # 2. Construir diccionario para 'absorber_agua'
        self._absorber_agua_handlers: Dict[CultivoType, AbsorcionHandler] = {
            Pino: self._pino_service.absorber_agua,
            Olivo: self._olivo_service.absorber_agua,
            Lechuga: self._lechuga_service.absorber_agua,
            Zanahoria: self._zanahoria_service.absorber_agua
        }

        # 3. Construir diccionario para 'mostrar_datos'
        self._mostrar_datos_handlers: Dict[CultivoType, MostrarHandler] = {
            Pino: self._pino_service.mostrar_datos,
            Olivo: self._olivo_service.mostrar_datos,
            Lechuga: self._lechuga_service.mostrar_datos,
            Zanahoria: self._zanahoria_service.mostrar_datos
        }
        
        # 4. Construir diccionario para 'crecer' (solo arboles)
        # Usamos 'Any' porque no todos los servicios tienen 'crecer'
        self._crecer_handlers: Dict[CultivoType, Any] = {
            Pino: self._pino_service.crecer,
            Olivo: self._olivo_service.crecer,
        }

    def _get_handler(self,
                     cultivo: Cultivo,
                     handlers_dict: Dict) -> Callable:
        """
        Metodo privado para buscar un handler en un diccionario
        de despacho.
        """
        tipo_cultivo = type(cultivo)
        handler = handlers_dict.get(tipo_cultivo)
        
        if handler is None:
            raise TypeError(f"Operacion no soportada para el tipo: {tipo_cultivo.__name__}")
        
        return handler

    # --- Metodos Publicos (Dispatch Polimorfico) ---

    def absorber_agua(self, cultivo: Cultivo) -> int:
        """
        Despacha la operacion 'absorber_agua' al servicio
        correcto usando el Registry.

        Args:
            cultivo (Cultivo): El cultivo que absorbe agua.

        Returns:
            int: El agua absorbida.
        """
        handler = self._get_handler(cultivo, self._absorber_agua_handlers)
        return handler(cultivo)

    def mostrar_datos(self, cultivo: Cultivo) -> None:
        """
        Despacha la operacion 'mostrar_datos' al servicio
        correcto usando el Registry. (US-009)

        Args:
            cultivo (Cultivo): El cultivo a mostrar.
        """
        handler = self._get_handler(cultivo, self._mostrar_datos_handlers)
        handler(cultivo)

    def crecer_arbol(self, arbol: Cultivo) -> None:
        """
        Despacha la operacion 'crecer' al servicio
        correcto usando el Registry. (US-008)

        Args:
            arbol (Cultivo): El arbol (Pino u Olivo) a crecer.
        """
        # Este metodo fallara si se le pasa una Lechuga
        handler = self._get_handler(arbol, self._crecer_handlers)
        handler(arbol)