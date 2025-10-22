"""
Modulo de la clase base abstracta CultivoService.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING

# Imports para la inyeccion del Strategy
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy

# Imports para type hints
if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo


class CultivoService(ABC):
    """
    Clase base abstracta para todos los servicios de cultivos.
    
    Implementa la logica de negocio comun a todos los cultivos,
    principalmente la absorcion de agua.
    
    Aqui se inyecta el patron Strategy (Rubrica 1.4, Rubrica Auto STRT-003).
    """

    def __init__(self, estrategia_absorcion: AbsorcionAguaStrategy):
        """
        Inicializa el servicio inyectando la estrategia de absorcion.

        Args:
            estrategia_absorcion (AbsorcionAguaStrategy): La estrategia
                concreta (ej. Seasonal o Constante) que este servicio usara.
        """
        self._estrategia_absorcion: AbsorcionAguaStrategy = estrategia_absorcion

    def absorber_agua(self, cultivo: Cultivo) -> int:
        """
        Calcula y aplica la absorcion de agua a un cultivo.
        
        Delega el calculo al patron Strategy inyectado.
        
        Args:
            cultivo (Cultivo): El cultivo que va a absorber agua.

        Returns:
            int: La cantidad de agua que fue absorbida.
        """
        # 1. Obtiene la fecha actual (necesaria para el strategy)
        fecha_actual = date.today()
        
        # 2. DELEGA el calculo al Strategy
        agua_absorbida = self._estrategia_absorcion.calcular_absorcion(
            fecha=fecha_actual,
            cultivo=cultivo
        )
        
        # 3. Aplica el resultado al cultivo
        if agua_absorbida > 0:
            agua_actual = cultivo.get_agua()
            cultivo.set_agua(agua_actual + agua_absorbida)
            
        return agua_absorbida

    @abstractmethod
    def mostrar_datos(self, cultivo: Cultivo) -> None:
        """
        Metodo abstracto para mostrar los datos especificos
        de cada tipo de cultivo (US-009).
        
        Sera implementado por las clases hijas.

        Args:
            cultivo (Cultivo): El cultivo a mostrar.
        """
        pass