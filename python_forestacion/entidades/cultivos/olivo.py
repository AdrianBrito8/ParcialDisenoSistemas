"""
Modulo de la entidad Olivo.
"""
from typing_extensions import override
from python_forestacion.entidades.cultivos.cultivo import Cultivo
from python_forestacion.entidades.cultivos.tipo_aceituna import TipoAceituna
from python_forestacion import constantes as C

class Olivo(Cultivo):
    """
    Entidad que representa un cultivo de tipo Olivo.
    Hereda de Cultivo y añade logica especifica de arboles (altura)
    y de olivos (tipo de aceituna).

    Referencia: US-005
    """

    def __init__(self, tipo_aceituna: TipoAceituna):
        """
        Inicializa un Olivo.

        Llama al constructor base con los valores de las constantes
        para superficie y agua inicial.

        Args:
            tipo_aceituna (TipoAceituna): El enum del tipo de aceituna.
        """
        super().__init__(
            superficie=C.SUPERFICIE_OLIVO,
            agua_inicial=C.AGUA_INICIAL_OLIVO
        )
        # US-005 especifica una altura inicial diferente para olivos
        self._altura: float = C.ALTURA_INICIAL_OLIVO 
        self._tipo_aceituna: TipoAceituna = tipo_aceituna

    @override
    def get_tipo(self) -> str:
        """
        Obtiene el tipo de cultivo.

        Returns:
            str: "Olivo"
        """
        return "Olivo"

    def get_altura(self) -> float:
        """
        Obtiene la altura actual del olivo.

        Returns:
            float: Altura en metros.
        """
        return self._altura

    def set_altura(self, altura: float) -> None:
        """
        Establece la altura del olivo.

        Args:
            altura (float): Nueva altura en metros.

        Raises:
            ValueError: Si la altura es negativa.
        """
        if altura < 0:
            raise ValueError("La altura no puede ser negativa")
        self._altura = altura

    def get_tipo_aceituna(self) -> TipoAceituna:
        """
        Obtiene el tipo de aceituna del olivo.

        Returns:
            TipoAceituna: El enum del tipo de aceituna.
        """
        return self._tipo_aceituna