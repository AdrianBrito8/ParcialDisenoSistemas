"""
Modulo de la entidad Pino.
"""
from typing_extensions import override
from python_forestacion.entidades.cultivos.cultivo import Cultivo
from python_forestacion import constantes as C

class Pino(Cultivo):
    """
    Entidad que representa un cultivo de tipo Pino.
    Hereda de Cultivo y añade logica especifica de arboles (altura)
    y de pinos (variedad).

    Referencia: US-004
    """

    def __init__(self, variedad: str):
        """
        Inicializa un Pino.

        Llama al constructor base con los valores de las constantes
        para superficie y agua inicial.

        Args:
            variedad (str): La variedad del pino (ej. Parana, Elliott).
        """
        super().__init__(
            superficie=C.SUPERFICIE_PINO,
            agua_inicial=C.AGUA_INICIAL_PINO
        )
        self._altura: float = C.ALTURA_INICIAL_ARBOL
        self._variedad: str = variedad

    @override
    def get_tipo(self) -> str:
        """
        Obtiene el tipo de cultivo.

        Returns:
            str: "Pino"
        """
        return "Pino"

    def get_altura(self) -> float:
        """
        Obtiene la altura actual del pino.

        Returns:
            float: Altura en metros.
        """
        return self._altura

    def set_altura(self, altura: float) -> None:
        """
        Establece la altura del pino.

        Args:
            altura (float): Nueva altura en metros.
        
        Raises:
            ValueError: Si la altura es negativa.
        """
        if altura < 0:
            raise ValueError("La altura no puede ser negativa")
        self._altura = altura

    def get_variedad(self) -> str:
        """
        Obtiene la variedad del pino.

        Returns:
            str: La variedad (ej. "Parana").
        """
        return self._variedad