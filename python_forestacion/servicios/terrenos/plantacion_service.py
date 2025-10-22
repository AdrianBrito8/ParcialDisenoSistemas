"""
Modulo del servicio PlantacionService.
Este es un servicio central que orquesta la logica de plantacion y riego.
"""
from typing import TYPE_CHECKING, List

# --- Imports de Patrones ---
# 1. Importa el Factory para crear cultivos (US-TECH-002)
from python_forestacion.patrones.factory.cultivo_factory import CultivoFactory

# 2. Importa el Registry (Singleton) para operar sobre cultivos (US-TECH-005)
from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry

# --- Imports de Entidades ---
from python_forestacion.entidades.terrenos.plantacion import Plantacion
from python_forestacion.entidades.cultivos.cultivo import Cultivo

# --- Imports de Excepciones ---
from python_forestacion.excepciones.superficie_insuficiente_exception import SuperficieInsuficienteException
from python_forestacion.excepciones.agua_agotada_exception import AguaAgotadaException
from python_forestacion.excepciones import mensajes_exception as MSG

# --- Imports de Constantes ---
from python_forestacion import constantes as C

if TYPE_CHECKING:
    # Para type hints
    from python_forestacion.entidades.cultivos.pino import Pino
    from python_forestacion.entidades.cultivos.olivo import Olivo
    # TypeAlias para Arbol
    Arbol = Pino | Olivo


class PlantacionService:
    """
    Servicio para gestionar la logica de negocio de las Plantaciones.
    
    Orquesta la plantacion de nuevos cultivos (usando Factory)
    y el riego de cultivos existentes (usando Registry/Strategy).
    """

    def __init__(self):
        """
        Inicializa el PlantacionService.
        
        Obtiene la instancia unica (Singleton) del Registry.
        """
        # Obtiene la instancia unica del Registry (Singleton)
        self._registry = CultivoServiceRegistry.get_instance()

    def plantar(self,
                plantacion: Plantacion,
                especie: str,
                cantidad: int) -> List[Cultivo]:
        """
        Planta una cantidad N de una especie de cultivo en la plantacion.
        
        Logica de negocio de US-004, US-005, US-006, US-007.
        Utiliza el CultivoFactory (Rubrica 1.2).

        Args:
            plantacion (Plantacion): La plantacion donde se plantara.
            especie (str): El nombre de la especie (ej. "Pino").
            cantidad (int): Cuantos cultivos plantar.

        Raises:
            SuperficieInsuficienteException: Si no hay espacio.
            ValueError: Si la cantidad es <= 0.

        Returns:
            List[Cultivo]: La lista de cultivos que fueron creados y plantados.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a plantar debe ser positiva")

        print(f"\n--- Intentando plantar {cantidad} x {especie} ---")
        
        # 1. Usa el Factory para crear un "prototipo" y ver su superficie
        #    No usamos el prototipo, solo lo usamos para leer sus datos.
        prototipo = CultivoFactory.crear_cultivo(especie)
        superficie_requerida = prototipo.get_superficie() * cantidad
        
        # 2. Validacion de superficie (US-004)
        superficie_disponible = plantacion.get_superficie_disponible()
        
        if superficie_disponible < superficie_requerida:
            raise SuperficieInsuficienteException(
                mensaje_tecnico=MSG.TEC_SUPERFICIE_INSUFICIENTE.format(
                    superficie_disponible, superficie_requerida),
                mensaje_usuario=MSG.USR_SUPERFICIE_INSUFICIENTE
            )

        # 3. Creacion y adicion
        cultivos_plantados = []
        for _ in range(cantidad):
            # Usa el Factory para crear la instancia real
            nuevo_cultivo = CultivoFactory.crear_cultivo(especie)
            plantacion.add_cultivo(nuevo_cultivo)
            cultivos_plantados.append(nuevo_cultivo)
            
        # 4. Actualizar superficie ocupada en la plantacion
        superficie_ocupada = plantacion.get_superficie_ocupada()
        plantacion.set_superficie_ocupada(
            superficie_ocupada + superficie_requerida
        )
        
        print(f"Plantacion exitosa. Superficie restante: "
              f"{plantacion.get_superficie_disponible():.2f} m²")
        
        return cultivos_plantados

    def regar(self, plantacion: Plantacion) -> None:
        """
        Riega todos los cultivos de la plantacion.
        
        Logica de negocio de US-008.
        Usa el Registry para despachar la absorcion y el crecimiento.

        Args:
            plantacion (Plantacion): La plantacion a regar.
            
        Raises:
            AguaAgotadaException: Si no hay agua para el riego.
        """
        
        # 1. Validar y consumir agua de la plantacion (US-008)
        agua_necesaria = C.AGUA_POR_RIEGO
        agua_disponible = plantacion.get_agua_disponible()
        
        if agua_disponible < agua_necesaria:
            raise AguaAgotadaException(
                mensaje_tecnico=MSG.TEC_AGUA_AGOTADA.format(
                    agua_disponible, agua_necesaria),
                mensaje_usuario=MSG.USR_AGUA_AGOTADA
            )
            
        plantacion.set_agua_disponible(agua_disponible - agua_necesaria)
        
        print(f"Riego iniciado. Consumiendo {agua_necesaria}L de la finca...")

        # 2. Distribuir agua a cada cultivo
        for cultivo in plantacion.get_cultivos():
            
            # 3. Llama al Registry (que llama al Strategy)
            agua_absorbida = self._registry.absorber_agua(cultivo)
            
            # 4. Llama al Registry para crecer (solo si es Arbol)
            # (Usamos 'from .pino import Pino' para evitar 'isinstance')
            from python_forestacion.entidades.cultivos.pino import Pino
            from python_forestacion.entidades.cultivos.olivo import Olivo
            
            if type(cultivo) in (Pino, Olivo):
                # Es un Arbol, llamamos a crecer
                self._registry.crecer_arbol(cultivo) # type: ignore
                
        print(f"Riego completado. Agua restante en finca: "
              f"{plantacion.get_agua_disponible()}L")