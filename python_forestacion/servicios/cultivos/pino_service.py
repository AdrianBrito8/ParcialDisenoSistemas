"""
Modulo del servicio concreto PinoService.
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
    from python_forestacion.entidades.cultivos.pino import Pino


class PinoService(ArbolService):
    """
    Servicio concreto para la logica de negocio de los Pinos.
    
    Hereda de ArbolService.
    Inyecta la estrategia de absorcion estacional (Seasonal).
    """

    def __init__(self):
        """
        Inicializa el PinoService.
        
        Aqui se realiza la INYECCION de la estrategia concreta
        (AbsorcionSeasonalStrategy) en la clase base,
        cumpliendo con la Rubrica 1.4.
        """
        # Inyecta la estrategia estacional
        super().__init__(AbsorcionSeasonalStrategy())

    @override
    def mostrar_datos(self, cultivo: 'Pino') -> None:
        """
        Muestra los datos especificos de un Pino.
        Implementacion de US-009.

        Args:
            cultivo (Pino): La entidad Pino a mostrar.
        """
        # 1. Llama a la implementacion base de ArbolService
        #    (que imprime ID, Tipo, Agua, Superficie, Altura)
        super().mostrar_datos(cultivo)
        
        # 2. Imprime los datos especificos de Pino
        print(f"Variedad: {cultivo.get_variedad()}")

    def crecer(self, arbol: 'Pino') -> None:
        """
        Metodo sobrecargado para aplicar el crecimiento especifico del Pino.
        Logica de negocio de US-008.

        Args:
            arbol (Pino): El pino que va a crecer.
        """
        # Llama al metodo 'crecer' de la clase base (ArbolService)
        # pasandole la cantidad de crecimiento especifica del pino
        # definida en constantes.py
        super().crecer(arbol, C.CRECIMIENTO_PINO_POR_RIEGO)