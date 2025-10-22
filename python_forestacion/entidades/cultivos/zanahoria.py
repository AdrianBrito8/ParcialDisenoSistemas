"""
Modulo de la entidad Zanahoria.
"""
from typing_extensions import override
from python_forestacion.entidades.cultivos.cultivo import Cultivo
from python_forestacion import constantes as C

class Zanahoria(Cultivo):
    """
    Entidad que representa un cultivo de tipo Zanahoria.
    Hereda de Cultivo y añade logica especifica de hortalizas
    (baby carrot, invernadero).

    Referencia: US-007
    """

    def __init__(self, is_baby_carrot: bool):
        """
        Inicializa una Zanahoria.

        Llama al constructor base con los valores de las constantes
        para superficie y agua inicial (0L segun US-007).

        Args:
            is_baby_carrot (bool): True si es baby carrot, False si es regular.
        """
        super().__init__(
            superficie=C.SUPERFICIE_ZANAHORIA,
            agua_inicial=C.AGUA_INICIAL_ZANAHORIA
        )
        self._is_baby_carrot: bool = is_baby_carrot
        # US-007 especifica que las zanahorias son a campo abierto
        self._invernadero: bool = False

    @override
    def get_tipo(self) -> str:
        """
        Obtiene el tipo de cultivo.

        Returns:
            str: "Zanahoria"
        """
        return "Zanahoria"

    def is_baby_carrot(self) -> bool:
        """
        Indica si la zanahoria es de tipo "baby carrot".

        Returns:
            bool: True si es baby carrot.
        """
        return self._is_baby_carrot

    def is_invernadero(self) -> bool:
        """
        Indica si el cultivo es de invernadero.

        Returns:
            bool: True si es de invernadero, False en caso contrario.
        """
        return self._invernadero