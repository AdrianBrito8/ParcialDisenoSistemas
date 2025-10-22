"""
Modulo de la implementacion "Constante" del Strategy.
"""
from datetime import date
from typing_extensions import override
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy
from python_forestacion.entidades.cultivos.cultivo import Cultivo

class AbsorcionConstanteStrategy(AbsorcionAguaStrategy):
    """
    Estrategia de absorcion constante (para Hortalizas).

    Absorbe una cantidad fija de agua, definida en su constructor.

    Referencia: US-008, US-TECH-004
    """

    def __init__(self, cantidad_constante: int):
        """
        Inicializa la estrategia.

        Args:
            cantidad_constante (int): La cantidad fija de agua
                                      que absorbora (ej. 1L o 2L).
        
        Raises:
            ValueError: Si la cantidad es negativa.
        """
        if cantidad_constante < 0:
            raise ValueError("La cantidad constante de absorcion no puede ser negativa")
        self._cantidad: int = cantidad_constante

    @override
    def calcular_absorcion(
        self,
        fecha: date,
        cultivo: 'Cultivo'
    ) -> int:
        """
        Devuelve la cantidad constante definida en el constructor.

        Args:
            fecha (date): No se usa en esta estrategia.
            cultivo (Cultivo): No se usa en esta estrategia.

        Returns:
            int: La cantidad de agua absorbida (ej. 1L o 2L).
        """
        return self._cantidad