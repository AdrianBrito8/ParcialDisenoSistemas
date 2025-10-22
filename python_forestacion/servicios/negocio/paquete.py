"""
Modulo de la entidad generica Paquete.
"""
from typing import Generic, List, TypeVar, Type

# T es un TypeVar, lo que permite la creacion de Generics
T = TypeVar('T')

class Paquete(Generic[T]):
    """
    Entidad generica que representa un paquete (caja) de
    cultivos cosechados.
    
    Usa Generic[T] para ser tipo-seguro (ej. Paquete[Pino],
    Paquete[Lechuga]).
    
    Referencia: US-020
    """
    _contador_id: int = 0

    def __init__(self, tipo_contenido: Type[T]):
        """
        Inicializa un paquete vacio.

        Args:
            tipo_contenido (Type[T]): El tipo de cultivo que
                                      contendra este paquete.
        """
        Paquete._contador_id += 1
        self._id_paquete: int = Paquete._contador_id
        self._tipo_contenido: Type[T] = tipo_contenido
        self._contenido: List[T] = []

    def get_id_paquete(self) -> int:
        """Obtiene el ID unico del paquete."""
        return self._id_paquete

    def get_tipo_contenido(self) -> Type[T]:
        """Obtiene el TIPO de contenido (ej. <class 'Pino'>)."""
        return self._tipo_contenido
    
    def get_nombre_tipo_contenido(self) -> str:
        """Obtiene el nombre legible del tipo (ej. 'Pino')."""
        return self._tipo_contenido.__name__

    def get_contenido(self) -> List[T]:
        """Obtiene la lista de items dentro del paquete."""
        return self._contenido.copy()

    def add_item(self, item: T) -> None:
        """Añade un item al paquete."""
        self._contenido.append(item)
        
    def add_items(self, items: List[T]) -> None:
        """Añade una lista de items al paquete."""
        self._contenido.extend(items)

    def get_cantidad(self) -> int:
        """Obtiene la cantidad de items en el paquete."""
        return len(self._contenido)

    def mostrar_contenido_caja(self) -> None:
        """
        Imprime un resumen del contenido del paquete.
        Implementacion de US-020.
        """
        print("\nContenido de la caja:")
        print(f"  Tipo: {self.get_nombre_tipo_contenido()}")
        print(f"  Cantidad: {self.get_cantidad()}")
        print(f"  ID Paquete: {self.get_id_paquete()}")