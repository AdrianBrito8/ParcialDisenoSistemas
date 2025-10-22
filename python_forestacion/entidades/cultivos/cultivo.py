"""
Modulo de la clase base abstracta Cultivo.
"""
from abc import ABC, abstractmethod

class Cultivo(ABC):
    """
    Clase base abstracta para todos los tipos de cultivos.

    Define la interfaz comun que debe tener cualquier cultivo,
    incluyendo superficie, agua y un ID unico.
    """

    # Variable de clase para autoincrementar el ID
    _contador_id: int = 0

    def __init__(self, superficie: float, agua_inicial: int):
        """
        Inicializa un nuevo cultivo.

        Args:
            superficie (float): La superficie en m² que ocupa el cultivo.
            agua_inicial (int): La cantidad de agua en litros que tiene al ser plantado.

        Raises:
            ValueError: Si la superficie es <= 0 o el agua inicial es < 0.
        """
        if superficie <= 0:
            raise ValueError("La superficie debe ser mayor a cero")
        if agua_inicial < 0:
            raise ValueError("El agua inicial no puede ser negativa")
        
        Cultivo._contador_id += 1
        self._id: int = Cultivo._contador_id
        self._superficie: float = superficie
        self._agua: int = agua_inicial

    def get_id(self) -> int:
        """
        Obtiene el ID unico del cultivo.

        Returns:
            int: El ID.
        """
        return self._id

    def get_superficie(self) -> float:
        """
        Obtiene la superficie que ocupa el cultivo.

        Returns:
            float: La superficie en m².
        """
        return self._superficie

    def get_agua(self) -> int:
        """
        Obtiene la cantidad de agua almacenada por el cultivo.

        Returns:
            int: Agua en litros.
        """
        return self._agua

    def set_agua(self, cantidad: int) -> None:
        """
        Establece la cantidad de agua del cultivo.

        Args:
            cantidad (int): Nueva cantidad de agua en litros.

        Raises:
            ValueError: Si la cantidad es negativa.
        """
        if cantidad < 0:
            raise ValueError("La cantidad de agua no puede ser negativa")
        self._agua = cantidad

    @abstractmethod
    def get_tipo(self) -> str:
        """
        Metodo abstracto para obtener el tipo de cultivo.
        Debe ser implementado por las clases hijas.

        Returns:
            str: El nombre del tipo de cultivo (ej. "Pino", "Lechuga").
        """
        pass