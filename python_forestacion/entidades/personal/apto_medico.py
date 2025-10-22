"""
Modulo de la entidad AptoMedico.
"""
from datetime import date

class AptoMedico:
    """
    Entidad que representa el certificado de aptitud medica
    de un trabajador.

    Referencia: US-015
    """

    def __init__(self,
                 apto: bool,
                 fecha_emision: date,
                 observaciones: str | None = None):
        """
        Inicializa el AptoMedico.

        Args:
            apto (bool): True si esta apto, False si no.
            fecha_emision (date): Fecha de emision del certificado.
            observaciones (str | None, optional): Observaciones medicas.
        """
        self._apto: bool = apto
        self._fecha_emision: date = fecha_emision
        self._observaciones: str | None = observaciones

    def esta_apto(self) -> bool:
        """
        Indica si el trabajador esta apto.

        Returns:
            bool: True si esta apto.
        """
        return self._apto

    def get_fecha_emision(self) -> date:
        """Obtiene la fecha de emision del certificado."""
        return self._fecha_emision

    def get_observaciones(self) -> str | None:
        """Obtiene las observaciones medicas, si existen."""
        return self._observaciones