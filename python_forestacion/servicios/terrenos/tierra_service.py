"""
Modulo del servicio TierraService.
"""
from python_forestacion.entidades.terrenos.tierra import Tierra
from python_forestacion.entidades.terrenos.plantacion import Plantacion

class TierraService:
    """
    Servicio para gestionar la logica de negocio de las Tierras.
    """

    def crear_tierra_con_plantacion(
        self,
        id_padron_catastral: int,
        superficie: float,
        domicilio: str,
        nombre_plantacion: str
    ) -> Tierra:
        """
        Crea una entidad Tierra y su Plantacion asociada,
        y las vincula.
        
        Logica de negocio de US-001 y US-002.

        Args:
            id_padron_catastral (int): ID de padron.
            superficie (float): Superficie en m².
            domicilio (str): Domicilio del terreno.
            nombre_plantacion (str): Nombre para la plantacion.

        Returns:
            Tierra: La entidad Tierra creada y ya vinculada.
        """
        
        # 1. Crear la Tierra
        tierra = Tierra(
            id_padron_catastral=id_padron_catastral,
            superficie=superficie,
            domicilio=domicilio
        )
        
        # 2. Crear la Plantacion
        plantacion = Plantacion(
            nombre=nombre_plantacion,
            superficie_maxima=superficie, # La plantacion usa la superficie de la tierra
            tierra=tierra
        )
        
        # 3. Vincular la Tierra con su Plantacion
        # (Esto es clave para que el modelo este completo)
        tierra.set_finca(plantacion)
        
        print(f"Tierra creada (Padron {id_padron_catastral}) "
              f"con Plantacion '{nombre_plantacion}'.")
        
        return tierra