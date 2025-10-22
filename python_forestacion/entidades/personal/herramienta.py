"""
Modulo de la entidad Herramienta.
"""

class Herramienta:
    """
    Entidad que representa una herramienta de trabajo.

    Referencia: US-016
    """

    def __init__(self,
                 id_herramienta: int,
                 nombre: str,
                 certificado_hys: bool):
        """
        Inicializa la Herramienta.

        Args:
            id_herramienta (int): ID unico de la herramienta.
            nombre (str): Nombre de la herramienta (ej. "Pala").
            certificado_hys (bool): Si posee certificado de Higiene y Seguridad.
        """
        self._id_herramienta: int = id_herramienta
        self._nombre: str = nombre
        self._certificado_hys: bool = certificado_hys

    def get_id_herramienta(self) -> int:
        """Obtiene el ID de la herramienta."""
        return self._id_herramienta

    def get_nombre(self) -> str:
        """Obtiene el nombre de la herramienta."""
        return self._nombre

    def tiene_certificado(self) -> bool:
        """Indica si la herramienta tiene certificado HyS."""
        return self._certificado_hys