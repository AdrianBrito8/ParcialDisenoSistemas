"""
Modulo del servicio FincasService.
Maneja la logica de negocio de alto nivel que
involucra a multiples fincas (registros).
"""
from typing import Dict, List, Type, TypeVar, cast

# --- Imports de Entidades y Servicios de Negocio ---
from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal
from python_forestacion.entidades.terrenos.plantacion import Plantacion
from python_forestacion.entidades.cultivos.cultivo import Cultivo
from python_forestacion.servicios.negocio.paquete import Paquete

# --- Imports para Type Hints ---
# T es el TypeVar para la cosecha generica
T = TypeVar('T', bound=Cultivo)


class FincasService:
    """
    Servicio para gestionar operaciones de alto nivel
    que afectan a multiples fincas (Registros Forestales).
    
    Implementa US-018, US-019 y US-020.
    """

    def __init__(self):
        """
        Inicializa el FincasService.
        
        Mantiene un diccionario interno de todas las fincas
        gestionadas, usando el ID de padron como clave.
        
        Referencia: US-018
        """
        self._fincas_gestionadas: Dict[int, RegistroForestal] = {}

    def add_finca(self, registro: RegistroForestal) -> None:
        """
        Agrega una finca (RegistroForestal) al servicio
        para que sea gestionada.
        
        Referencia: US-018

        Args:
            registro (RegistroForestal): El registro a gestionar.
        """
        id_padron = registro.get_id_padron()
        if id_padron not in self._fincas_gestionadas:
            self._fincas_gestionadas[id_padron] = registro
            print(f"Finca (Padron {id_padron}) agregada al servicio de gestion.")
        else:
            print(f"Finca (Padron {id_padron}) ya estaba siendo gestionada.")

    def buscar_finca(self, id_padron: int) -> RegistroForestal | None:
        """
        Busca una finca gestionada por su ID de padron.
        
        Referencia: US-018
        
        Args:
            id_padron (int): El ID de padron a buscar.

        Returns:
            RegistroForestal | None: El registro si se encuentra, o None.
        """
        return self._fincas_gestionadas.get(id_padron)

    def fumigar(self, id_padron: int, plaguicida: str) -> bool:
        """
        Aplica una fumigacion a todos los cultivos de una finca.
        
        Implementacion de US-019.

        Args:
            id_padron (int): El padron de la finca a fumigar.
            plaguicida (str): El nombre del plaguicida a aplicar.

        Returns:
            bool: True si la fumigacion fue exitosa, False si
                  no se encontro la finca.
        """
        print(f"\n--- Intentando fumigar finca {id_padron} ---")
        registro = self.buscar_finca(id_padron)
        
        if registro is None:
            print(f"Error: Finca {id_padron} no encontrada.")
            return False
            
        # Logica de fumigacion (aqui solo imprimimos)
        print(f"Fumigando plantacion '{registro.get_plantacion().get_nombre()}' "
              f"con: {plaguicida}.")
        return True

    def cosechar_yempaquetar(self, tipo_cultivo: Type[T]) -> Paquete[T]:
        """
        Cosecha TODOS los cultivos de un TIPO especifico de
        TODAS las fincas gestionadas y los guarda en un Paquete.
        
        Implementacion de US-020.

        Args:
            tipo_cultivo (Type[T]): El tipo de cultivo a cosechar
                                    (ej. Lechuga, Pino).

        Returns:
            Paquete[T]: Un paquete tipo-seguro con los cultivos cosechados.
        """
        print(f"\n--- COSECHANDO todas las {tipo_cultivo.__name__} ---")
        
        # 1. Crear el paquete generico vacio (US-020)
        paquete_cosecha: Paquete[T] = Paquete(tipo_cultivo)
        
        cultivos_cosechados: List[T] = []

        # 2. Iterar por TODAS las fincas gestionadas
        for registro in self._fincas_gestionadas.values():
            plantacion = registro.get_plantacion()
            superficie_liberada = 0.0
            
            # 3. Iterar por todos los cultivos de ESA finca
            # (Iteramos sobre una copia para poder modificar la original)
            for cultivo in plantacion.get_cultivos(): 
                
                # 4. Comprobar si es del tipo buscado
                if isinstance(cultivo, tipo_cultivo):
                    # ¡Es del tipo! Lo cosechamos.
                    # Hacemos 'cast' para ayudar al type checker
                    cultivo_cosechado = cast(T, cultivo)
                    
                    cultivos_cosechados.append(cultivo_cosechado)
                    
                    # 5. Removerlo de la plantacion (US-020)
                    plantacion.remove_cultivo(cultivo_cosechado)
                    
                    # 6. Contabilizar superficie liberada
                    superficie_liberada += cultivo_cosechado.get_superficie()

            # 7. Actualizar superficie de la plantacion
            if superficie_liberada > 0:
                superficie_actual = plantacion.get_superficie_ocupada()
                plantacion.set_superficie_ocupada(
                    superficie_actual - superficie_liberada
                )
                print(f"  Liberados {superficie_liberada:.2f} m² "
                      f"en {plantacion.get_nombre()}.")

        # 8. Guardar todo en el paquete
        paquete_cosecha.add_items(cultivos_cosechados)
        
        print(f"COSECHA TOTAL: {paquete_cosecha.get_cantidad()} "
              f"unidades de {tipo_cultivo.__name__}.")
              
        return paquete_cosecha