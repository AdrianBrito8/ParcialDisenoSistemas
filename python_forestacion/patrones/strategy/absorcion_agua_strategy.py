"""
Modulo de la interfaz abstracta (Strategy) AbsorcionAguaStrategy.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING

# Para type hints sin importacion circular
if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo

class AbsorcionAguaStrategy(ABC):
    """
    Interfaz (Strategy) para definir algoritmos intercambiables
    de absorcion de agua.

    Referencia: US-TECH-004, Rubrica 1.4
    """

    @abstractmethod
    def calcular_absorcion(
        self,
        fecha: date,
        cultivo: 'Cultivo'
    ) -> int:
        """
        Calcula la cantidad de agua absorbida por un cultivo
        en funcion de la estrategia.

        Args:
            fecha (date): La fecha actual (para estrategias estacionales).
            cultivo (Cultivo): El cultivo que esta absorbiendo agua.

        Returns:
            int: La cantidad de agua absorbida en litros.
        """
        pass