"""
Modulo del servicio concreto OlivoService.
"""
from typing import TYPE_CHECKING
from typing_extensions import override

# Imports base
from python_forestacion.servicios.cultivos.arbol_service import ArbolService

# Imports para inyectar el Strategy
from python_forestacion.patrones.strategy.impl.absorcion_seasonal_strategy import AbsorcionSeasonalStrategy

# Imports para constantes
from python_forestacion import constantes as C

# Imports para type hints
if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.olivo import Olivo


class OlivoService(ArbolService):
    """
    Servicio concreto para la logica de negocio de los Olivos.
    
    Hereda de ArbolService.
    Inyecta la estrategia de absorcion estacional (Seasonal).
    """

    def __init__(self):
        """
        Inicializa el OlivoService.
        
        Inyecta la estrategia estacional (Seasonal).
        """
        # Inyecta la misma estrategia que Pino
        super().__init__(AbsorcionSeasonalStrategy())

    @override
    def mostrar_datos(self, cultivo: Olivo) -> None:
        """
        Muestra los datos especificos de un Olivo.
        Implementacion de US-009.

        Args:
            cultivo (Olivo): La entidad Olivo a mostrar.
        """
        # 1. Llama a la implementacion base de ArbolService
        super().mostrar_datos(cultivo)
        
        # 2. Imprime los datos especificos de Olivo
        print(f"Tipo de aceituna: {cultivo.get_tipo_aceituna().value}")

    def crecer(self, arbol: Olivo) -> None:
        """
        Metodo sobrecargado para aplicar el crecimiento especifico del Olivo.
        Logica de negocio de US-008.

        Args:
            arbol (Olivo): El olivo que va a crecer.
        """
        # Llama al metodo 'crecer' de la clase base (ArbolService)
        # pasandole la cantidad de crecimiento especifica del olivo
        # definida en constantes.py
        super().crecer(arbol, C.CRECIMIENTO_OLIVO_POR_RIEGO)