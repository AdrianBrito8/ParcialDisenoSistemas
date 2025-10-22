"""
Modulo de la entidad RegistroForestal.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.tierra import Tierra
    from python_forestacion.entidades.terrenos.plantacion import Plantacion

class RegistroForestal:
    """
    Entidad que representa el registro oficial completo de la finca.

    Agrupa la Tierra, la Plantacion, el Propietario y el Avaluo.
    Esta es la entidad principal que se persiste en disco.

    Referencia: US-003
    """

    def __init__(self,
                 id_padron: int,
                 tierra: Tierra,
                 plantacion: Plantacion,
                 propietario: str,
                 avaluo: float):
        """
        Inicializa el Registro Forestal.

        Args:
            id_padron (int): ID de padron (debe coincidir con el de Tierra).
            tierra (Tierra): La entidad Tierra.
            plantacion (Plantacion): La entidad Plantacion.
            propietario (str): Nombre del propietario.
            avaluo (float): Avaluo fiscal.

        Raises:
            ValueError: Si el avaluo es <= 0.
        """
        if avaluo <= 0:
            raise ValueError("El avaluo fiscal debe ser positivo")
        
        self._id_padron: int = id_padron
        self._tierra: Tierra = tierra
        self._plantacion: Plantacion = plantacion
        self._propietario: str = propietario
        self._avaluo: float = avaluo

    def get_id_padron(self) -> int:
        """Obtiene el ID del padron."""
        return self._id_padron

    def get_tierra(self) -> Tierra:
        """Obtiene la entidad Tierra."""
        return self._tierra

    def get_plantacion(self) -> Plantacion:
        """Obtiene la entidad Plantacion."""
        return self._plantacion

    def get_propietario(self) -> str:
        """Obtiene el nombre del propietario."""
        return self._propietario

    def get_avaluo(self) -> float:
        """Obtiene el avaluo fiscal."""
        return self._avaluo