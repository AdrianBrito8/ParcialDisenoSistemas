"""
Modulo de la entidad Lechuga.
"""
from typing_extensions import override
from python_forestacion.entidades.cultivos.cultivo import Cultivo
from python_forestacion import constantes as C

class Lechuga(Cultivo):
    """
    Entidad que representa un cultivo de tipo Lechuga.
    Hereda de Cultivo y añade logica especifica de hortalizas
    (variedad, invernadero).

    Referencia: US-006
    """

    def __init__(self, variedad: str):
        """
        Inicializa una Lechuga.

        Llama al constructor base con los valores de las constantes
        para superficie y agua inicial.

        Args:
            variedad (str): La variedad de la lechuga (ej. Crespa, Mantecosa).
        """
        super().__init__(superficie=C.SUPERFICIE_LECHUGA,
            agua_inicial=C.AGUA_INICIAL_LECHUGA
        )
        self._variedad: str = variedad
        # US-006 especifica que las lechugas son siempre de invernadero
        self._invernadero: bool = True

    @override
    def get_tipo(self) -> str:
        """
        Obtiene el tipo de cultivo.

        Returns:
            str: "Lechuga"
        """
        return "Lechuga"

    def get_variedad(self) -> str:
        """
        Obtiene la variedad de la lechuga.

        Returns:
            str: La variedad.
        """
        return self._variedad

    def is_invernadero(self) -> bool:
        """
        Indica si el cultivo es de invernadero.

        Returns:
            bool: True si es de invernadero, False en caso contrario.
        """
        return self._invernadero