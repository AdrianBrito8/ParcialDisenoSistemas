"""
Modulo de la Excepcion SuperficieInsuficienteException
"""
from .forestacion_exception import ForestacionException

class SuperficieInsuficienteException(ForestacionException):
    """
    Excepcion lanzada cuando no hay suficiente superficie en la plantacion
    para plantar nuevos cultivos.
    """
    def __init__(self, mensaje_tecnico: str, mensaje_usuario: str):
        """
        Inicializa la excepcion de superficie insuficiente.

        Args:
            mensaje_tecnico (str): Mensaje tecnico detallado.
            mensaje_usuario (str): Mensaje amigable para el usuario.
        """
        super().__init__(mensaje_tecnico, mensaje_usuario)