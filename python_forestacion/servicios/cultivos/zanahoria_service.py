"""
Modulo del servicio concreto ZanahoriaService.
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
    from python_forestacion.entidades.cultivos.zanahoria import Zanahoria


class ZanahoriaService(CultivoService):
    """
    Servicio concreto para la logica de negocio de las Zanahorias.
    
    Hereda de CultivoService (la base).
    Inyecta la estrategia de absorcion constante.
    """

    def __init__(self):
        """
        Inicializa el ZanahoriaService.
        
        Inyecta la estrategia constante pasandole la cantidad
        especifica de la zanahoria (2L).
        
        Referencia: US-008, Rubrica 1.4
        """
        # Inyecta la estrategia constante con 2L
        super().__init__(
            AbsorcionConstanteStrategy(C.ABSORCION_CONSTANTE_ZANAHORIA)
        )

    @override
    def mostrar_datos(self, cultivo: 'Zanahoria') -> None:
        """
        Muestra los datos especificos de una Zanahoria.
        Implementacion de US-009.

        Args:
            cultivo (Zanahoria): La entidad Zanahoria a mostrar.
        """
        # Imprime los datos base
        print(f"Cultivo: {cultivo.get_tipo()}")
        print(f"Superficie: {cultivo.get_superficie()} m²")
        print(f"Agua almacenada: {cultivo.get_agua()} L")
        
        # Imprime los datos especificos de Zanahoria
        print(f"Es baby carrot: {cultivo.is_baby_carrot()}")