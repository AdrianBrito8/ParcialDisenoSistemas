"""
Modulo de la implementacion "Seasonal" del Strategy.
"""
from datetime import date
from typing_extensions import override
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy
from python_forestacion.entidades.cultivos.cultivo import Cultivo
from python_forestacion import constantes as C

class AbsorcionSeasonalStrategy(AbsorcionAguaStrategy):
    """
    Estrategia de absorcion estacional (para Arboles).

    - Verano (Marzo a Agosto): Absorbe 5L
    - Invierno (Resto): Absorbe 2L

    Referencia: US-008, US-TECH-004
    """

    @override
    def calcular_absorcion(
        self,
        fecha: date,
        cultivo: 'Cultivo'
    ) -> int:
        """
        Calcula la absorcion basandose en el mes.

        Args:
            fecha (date): La fecha actual.
            cultivo (Cultivo): El cultivo (no se usa aqui, pero lo pide la interfaz).

        Returns:
            int: Cantidad de agua absorbida (5L o 2L).
        """
        mes = fecha.month
        
        # Logica de US-008, usando constantes de C
        if C.MES_INICIO_VERANO <= mes <= C.MES_FIN_VERANO:
            return C.ABSORCION_SEASONAL_VERANO # 5L
        else:
            return C.ABSORCION_SEASONAL_INVIERNO # 2L