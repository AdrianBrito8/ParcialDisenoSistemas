"""
Modulo de la entidad Plantacion (Finca).
"""
from __future__ import annotations
from typing import List, TYPE_CHECKING

# Se usa TYPE_CHECKING para evitar importaciones circulares
if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo
    from python_forestacion.entidades.personal.trabajador import Trabajador
    from python_forestacion.entidades.terrenos.tierra import Tierra

class Plantacion:
    """
    Entidad que representa la plantacion o finca.

    Contiene la logica de gestion de superficie, agua,
    y las listas de cultivos y trabajadores.

    Referencia: US-002
    """
    AGUA_INICIAL_DEFAULT = 500 # Litros (de US-002)

    def __init__(self,
                 nombre: str,
                 superficie_maxima: float,
                 tierra: Tierra,
                 agua: int = AGUA_INICIAL_DEFAULT):
        """
        Inicializa la Plantacion.

        Args:
            nombre (str): Nombre identificatorio (ej. "Finca del Madero").
            superficie_maxima (float): Superficie total disponible (heredada de Tierra).
            tierra (Tierra): La instancia de Tierra a la que esta asociada.
            agua (int, optional): Agua disponible. Defaults a 500L.
        """
        self._nombre: str = nombre
        self._superficie_maxima: float = superficie_maxima
        self._superficie_ocupada: float = 0.0
        self._agua_disponible: int = agua
        self._tierra: Tierra = tierra
        
        self._cultivos: List[Cultivo] = []
        self._trabajadores: List[Trabajador] = []

    def get_nombre(self) -> str:
        """Obtiene el nombre de la plantacion."""
        return self._nombre

    def get_superficie_maxima(self) -> float:
        """Obtiene la superficie maxima permitida en m²."""
        return self._superficie_maxima

    def get_superficie_ocupada(self) -> float:
        """Obtiene la superficie actualmente ocupada por cultivos."""
        return self._superficie_ocupada

    def set_superficie_ocupada(self, superficie: float) -> None:
        """
        Establece la superficie ocupada.
        
        Args:
            superficie (float): Nueva superficie ocupada.

        Raises:
            ValueError: Si la superficie es < 0 o > superficie maxima.
        """
        if superficie < 0:
            raise ValueError("La superficie ocupada no puede ser negativa")
        if superficie > self._superficie_maxima:
            raise ValueError("La superficie ocupada no puede superar la maxima")
        self._superficie_ocupada = superficie
        
    def get_superficie_disponible(self) -> float:
        """
        Calcula y obtiene la superficie aun disponible.

        Returns:
            float: Superficie disponible en m².
        """
        return self._superficie_maxima - self._superficie_ocupada

    def get_agua_disponible(self) -> int:
        """Obtiene el agua disponible en la plantacion."""
        return self._agua_disponible

    def set_agua_disponible(self, agua: int) -> None:
        """
        Establece el agua disponible.
        Criterio de aceptacion de US-002.

        Args:
            agua (int): Nueva cantidad de agua en litros.

        Raises:
            ValueError: Si el agua es negativa.
        """
        if agua < 0:
            raise ValueError("El agua no puede ser negativa")
        self._agua_disponible = agua
        
    def get_tierra(self) -> Tierra:
        """Obtiene la entidad Tierra asociada."""
        return self._tierra

    # --- Gestion de Listas (con Copias Defensivas) ---

    def get_cultivos(self) -> List[Cultivo]:
        """
        Obtiene una COPIA de la lista de cultivos.
        (US-014, Rubrica 5.2: Defensive Copying)

        Returns:
            List[Cultivo]: Una copia de la lista de cultivos.
        """
        return self._cultivos.copy()

    def add_cultivo(self, cultivo: Cultivo) -> None:
        """Añade un cultivo a la plantacion."""
        self._cultivos.append(cultivo)

    def remove_cultivo(self, cultivo: Cultivo) -> None:
        """
        Remueve un cultivo de la plantacion.
        (Necesario para US-020: Cosechar)
        """
        if cultivo in self._cultivos:
            self._cultivos.remove(cultivo)

    def get_trabajadores(self) -> List[Trabajador]:
        """
        Obtiene una COPIA de la lista de trabajadores.
        (US-017, Rubrica 5.2: Defensive Copying)

        Returns:
            List[Trabajador]: Una copia de la lista de trabajadores.
        """
        return self._trabajadores.copy()

    def set_trabajadores(self, trabajadores: List[Trabajador]) -> None:
        """
        Establece la lista de trabajadores, guardando una COPIA.
        (US-017, Rubrica 5.2: Defensive Copying)
        
        Args:
            trabajadores (List[Trabajador]): La nueva lista de trabajadores.
        """
        self._trabajadores = trabajadores.copy()