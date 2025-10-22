"""
Modulo del Enum TipoAceituna.
"""
from enum import Enum

class TipoAceituna(Enum):
    """
    Enumera los tipos de aceituna permitidos para los Olivos.
    Referencia: US-005
    """
    ARBEQUINA = "Arbequina"
    PICUAL = "Picual"
    MANZANILLA = "Manzanilla"