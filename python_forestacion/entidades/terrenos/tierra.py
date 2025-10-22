"""
Modulo de la entidad Tierra.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

# Se usa TYPE_CHECKING para evitar importaciones circulares
# en tiempo de ejecucion.
if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.plantacion import Plantacion

class Tierra:
    """
    Entidad que representa un terreno forestal.

    Contiene informacion catastral, superficie y el domicilio.
    Esta vinculada a una (y solo una) plantacion.

    Referencia: US-001
    """

    def __init__(self,
                 id_padron_catastral: int,
                 superficie: float,
                 domicilio: str):
        """
        Inicializa la Tierra.

        Args:
            id_padron_catastral (int): Numero unico de padron.
            superficie (float): Superficie total en m².
            domicilio (str): Ubicacion fisica.

        Raises:
            ValueError: Si el padron es <= 0 o la superficie es <= 0.
        """
        if id_padron_catastral <= 0:
            raise ValueError("El padron catastral debe ser un numero positivo")
        if superficie <= 0:
            raise ValueError("La superficie debe ser mayor a cero")

        self._id_padron_catastral: int = id_padron_catastral
        self._superficie: float = superficie
        self._domicilio: str = domicilio
        self._finca: Plantacion | None = None # Se asigna post-creacion

    def get_id_padron_catastral(self) -> int:
        """Obtiene el ID del padron catastral."""
        return self._id_padron_catastral

    def get_superficie(self) -> float:
        """Obtiene la superficie total del terreno en m²."""
        return self._superficie

    def set_superficie(self, superficie: float) -> None:
        """
        Establece la superficie del terreno.
        Criterio de aceptacion de US-001.

        Args:
            superficie (float): Nueva superficie en m².

        Raises:
            ValueError: Si la superficie es <= 0.
        """
        if superficie <= 0:
            raise ValueError("La superficie debe ser mayor a cero")
        self._superficie = superficie

    def get_domicilio(self) -> str:
        """Obtiene el domicilio del terreno."""
        return self._domicilio

    def get_finca(self) -> Plantacion | None:
        """Obtiene la plantacion asociada a este terreno."""
        return self._finca

    def set_finca(self, plantacion: Plantacion) -> None:
        """
        Asigna la plantacion (finca) a este terreno.
        
        Args:
            plantacion (Plantacion): La instancia de la plantacion.
        """
        self._finca = plantacion