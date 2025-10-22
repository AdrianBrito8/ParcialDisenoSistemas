"""
Modulo de la entidad Tarea.
"""
from datetime import date
from enum import Enum

class EstadoTarea(Enum):
    """
    Enumera los estados posibles de una Tarea.
    """
    PENDIENTE = "Pendiente"
    COMPLETADA = "Completada"

class Tarea:
    """
    Entidad que representa una tarea agricola asignada.

    Referencia: US-014
    """

    def __init__(self,
                 id_tarea: int,
                 fecha: date,
                 descripcion: str):
        """
        Inicializa la Tarea.

        Args:
            id_tarea (int): ID unico de la tarea.
            fecha (date): Fecha programada para la tarea.
            descripcion (str): Descripcion (ej. "Desmalezar").
        """
        self._id_tarea: int = id_tarea
        self._fecha: date = fecha
        self._descripcion: str = descripcion
        self._estado: EstadoTarea = EstadoTarea.PENDIENTE # Siempre inicia PENDIENTE

    def get_id_tarea(self) -> int:
        """Obtiene el ID de la tarea."""
        return self._id_tarea

    def get_fecha(self) -> date:
        """Obtiene la fecha programada de la tarea."""
        return self._fecha

    def get_descripcion(self) -> str:
        """Obtiene la descripcion de la tarea."""
        return self._descripcion

    def get_estado(self) -> EstadoTarea:
        """Obtiene el estado actual de la tarea."""
        return self._estado

    def completar_tarea(self) -> None:
        """
        Marca la tarea como COMPLETADA.
        (Necesario para US-016)
        """
        self._estado = EstadoTarea.COMPLETADA