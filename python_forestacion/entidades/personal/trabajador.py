"""
Modulo de la entidad Trabajador.
"""
from typing import List
from python_forestacion.entidades.personal.tarea import Tarea
from python_forestacion.entidades.personal.apto_medico import AptoMedico

class Trabajador:
    """
    Entidad que representa a un trabajador agricola.

    Contiene sus datos personales, la lista de tareas asignadas
    y su certificado de apto medico.

    Referencia: US-014
    """

    def __init__(self,
                 dni: int,
                 nombre: str,
                 tareas: List[Tarea]):
        """
        Inicializa el Trabajador.

        Args:
            dni (int): DNI unico del trabajador.
            nombre (str): Nombre completo.
            tareas (List[Tarea]): Lista de tareas asignadas.
        
        Raises:
            ValueError: Si el DNI es <= 0.
        """
        if dni <= 0:
            raise ValueError("El DNI debe ser un numero positivo")
            
        self._dni: int = dni
        self._nombre: str = nombre
        
        # Guardamos una copia para cumplir con US-014 (inmutabilidad)
        self._tareas: List[Tarea] = tareas.copy()
        
        # US-014: Inicia sin apto medico
        self._apto_medico: AptoMedico | None = None

    def get_dni(self) -> int:
        """Obtiene el DNI del trabajador."""
        return self._dni

    def get_nombre(self) -> str:
        """Obtiene el nombre completo del trabajador."""
        return self._nombre

    def get_tareas(self) -> List[Tarea]:
        """
        Obtiene una COPIA de la lista de tareas.
        (US-014, Rubrica 5.2: Defensive Copying)

        Returns:
            List[Tarea]: Una copia de la lista de tareas.
        """
        return self._tareas.copy()

    def get_apto_medico(self) -> AptoMedico | None:
        """
        Obtiene el apto medico del trabajador, si existe.

        Returns:
            AptoMedico | None: El apto medico, o None si no tiene.
        """
        return self._apto_medico

    def set_apto_medico(self, apto: AptoMedico) -> None:
        """
        Asigna o actualiza el apto medico.
        (Necesario para US-015)

        Args:
            apto (AptoMedico): El nuevo certificado de apto medico.
        """
        self._apto_medico = apto