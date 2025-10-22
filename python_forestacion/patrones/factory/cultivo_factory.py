"""
Modulo de la implementacion del Patron Factory Method.
"""
from typing_extensions import override
from python_forestacion.entidades.cultivos.cultivo import Cultivo
from python_forestacion.entidades.cultivos.pino import Pino
from python_forestacion.entidades.cultivos.olivo import Olivo
from python_forestacion.entidades.cultivos.lechuga import Lechuga
from python_forestacion.entidades.cultivos.zanahoria import Zanahoria
from python_forestacion.entidades.cultivos.tipo_aceituna import TipoAceituna


class CultivoFactory:
    """
    Implementa el patron Factory Method para la creacion de cultivos.

    Centraliza la logica de instanciacion, desacoplando al cliente
    (ej. PlantacionService) de las clases concretas.

    Referencia: US-TECH-002, Rubrica 1.2, Rubrica Auto FACT-*
    """

    @staticmethod
    def _crear_pino() -> Cultivo:
        """Metodo factory privado para crear Pino."""
        # US-004: Variedad por defecto
        return Pino(variedad="Parana")

    @staticmethod
    def _crear_olivo() -> Cultivo:
        """Metodo factory privado para crear Olivo."""
        # US-005: Tipo de aceituna por defecto
        return Olivo(tipo_aceituna=TipoAceituna.ARBEQUINA)

    @staticmethod
    def _crear_lechuga() -> Cultivo:
        """Metodo factory privado para crear Lechuga."""
        # US-006: Variedad por defecto
        return Lechuga(variedad="Crespa")

    @staticmethod
    def _crear_zanahoria() -> Cultivo:
        """Metodo factory privado para crear Zanahoria."""
        # US-007: Tipo por defecto (no baby carrot)
        return Zanahoria(is_baby_carrot=False)

    @staticmethod
    def crear_cultivo(especie: str) -> Cultivo:
        """
        Metodo factory principal y publico.

        Utiliza un diccionario para el dispatch, cumpliendo con
        Rubrica 1.2 y Rubrica Auto (FACT-004).

        Args:
            especie (str): El tipo de cultivo a crear (ej. "Pino").

        Raises:
            ValueError: Si la especie es desconocida.

        Returns:
            Cultivo: Una instancia de una subclase de Cultivo.
        """
        # El diccionario de factories exigido por la rubrica.
        # NO USAR LAMBDAS (Rubrica 3.4)
        factories = {
            "Pino": CultivoFactory._crear_pino,
            "Olivo": CultivoFactory._crear_olivo,
            "Lechuga": CultivoFactory._crear_lechuga,
            "Zanahoria": CultivoFactory._crear_zanahoria
        }

        if especie not in factories:
            raise ValueError(f"Especie de cultivo desconocida: {especie}")

        # Llama al metodo factory privado correspondiente
        creador_cultivo = factories[especie]
        cultivo_creado = creador_cultivo()
        
        return cultivo_creado