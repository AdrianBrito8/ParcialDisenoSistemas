"""
Modulo de la Excepcion AguaAgotadaException
"""
from .forestacion_exception import ForestacionException

class AguaAgotadaException(ForestacionException):
    """
    Excepcion lanzada cuando no hay suficiente agua en la plantacion
    para realizar una operacion (ej. regar).
    """
    def __init__(self, mensaje_tecnico: str, mensaje_usuario: str):
        """
        Inicializa la excepcion de agua agotada.

        Args:
            mensaje_tecnico (str): Mensaje tecnico detallado.
            mensaje_usuario (str): Mensaje amigable para el usuario.
        """
        super().__init__(mensaje_tecnico, mensaje_usuario)