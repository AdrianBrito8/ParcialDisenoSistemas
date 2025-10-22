"""
Modulo de la clase base abstracta ArbolService.
Hereda de CultivoService y añade logica especifica de arboles.
"""
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing_extensions import override

# Imports base
from python_forestacion.servicios.cultivos.cultivo_service import CultivoService

# Imports para type hints
if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.pino import Pino
    from python_forestacion.entidades.cultivos.olivo import Olivo
    
# Definimos un TypeAlias para Arbol
Arbol = Pino | Olivo

class ArbolService(CultivoService):
    """
    Clase base abstracta para servicios de Arboles (Pino, Olivo).
    
    Hereda de CultivoService (reutilizando la inyeccion de Strategy
    y el metodo absorber_agua).
    
    Añade la logica de negocio 'crecer', comun a todos los arboles.
    Referencia: Rubrica 2.2 (Jerarquia de Clases)
    """

    @abstractmethod
    @override
    def mostrar_datos(self, cultivo: Arbol) -> None:
        """
        Metodo abstracto para mostrar datos (redefinido para Arbol).

        Args:
            cultivo (Arbol): El arbol (Pino u Olivo) a mostrar.
        """
        # Imprime la base comun a todos los arboles
        print(f"Cultivo: {cultivo.get_tipo()}")
        print(f"Superficie: {cultivo.get_superficie()} m²")
        print(f"Agua almacenada: {cultivo.get_agua()} L")
        print(f"ID: {cultivo.get_id()}")
        print(f"Altura: {cultivo.get_altura():.2f} m") # Formatea a 2 decimales

    def crecer(self, arbol: Arbol, cantidad_crecimiento: float) -> None:
        """
        Aplica el crecimiento a un arbol.
        Logica de negocio de US-008.

        Args:
            arbol (Arbol): El arbol que va a crecer.
            cantidad_crecimiento (float): La cantidad en metros a crecer.
        
        Raises:
            ValueError: Si la cantidad de crecimiento es negativa.
        """
        if cantidad_crecimiento < 0:
            raise ValueError("El crecimiento no puede ser negativo")
            
        altura_actual = arbol.get_altura()
        arbol.set_altura(altura_actual + cantidad_crecimiento)