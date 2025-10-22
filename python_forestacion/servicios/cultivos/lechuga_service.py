"""
Modulo del servicio concreto LechugaService.
"""
from typing import TYPE_CHECKING
from typing_extensions import override

# Imports base
from python_forestacion.servicios.cultivos.cultivo_service import CultivoService

# Imports para inyectar el Strategy
from python_forestacion.patrones.strategy.impl.absorcion_constante_strategy import AbsorcionConstanteStrategy

# Imports para constantes
from python_forestacion import constantes as C

# Imports para type hints
if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.lechuga import Lechuga


class LechugaService(CultivoService):
    """
    Servicio concreto para la logica de negocio de las Lechugas.
    
    Hereda de CultivoService (la base).
    Inyecta la estrategia de absorcion constante.
    """

    def __init__(self):
        """
        Inicializa el LechugaService.
        
        Aqui se realiza la INYECCION de la estrategia concreta
        (AbsorcionConstanteStrategy) pasandole la cantidad
        especifica de la lechuga (1L).
        
        Referencia: US-008, Rubrica 1.4
        """
        # Inyecta la estrategia constante con 1L
        super().__init__(
            AbsorcionConstanteStrategy(C.ABSORCION_CONSTANTE_LECHUGA)
        )

    @override
    def mostrar_datos(self, cultivo: 'Lechuga') -> None:
        """
        Muestra los datos especificos de una Lechuga.
        Implementacion de US-009.

        Args:
            cultivo (Lechuga): La entidad Lechuga a mostrar.
        """
        # Imprime los datos base
        print(f"Cultivo: {cultivo.get_tipo()}")
        print(f"Superficie: {cultivo.get_superficie()} m²")
        print(f"Agua almacenada: {cultivo.get_agua()} L")
        
        # Imprime los datos especificos de Lechuga
        print(f"Variedad: {cultivo.get_variedad()}")
        print(f"Invernadero: {cultivo.is_invernadero()}")