"""
Modulo del servicio TrabajadorService.
Maneja la logica de negocio de la gestion de personal.
"""
from datetime import date
from typing import List, TYPE_CHECKING

# --- Imports de Entidades ---
from python_forestacion.entidades.personal.trabajador import Trabajador
from python_forestacion.entidades.personal.apto_medico import AptoMedico
from python_forestacion.entidades.personal.tarea import Tarea, EstadoTarea

if TYPE_CHECKING:
    from python_forestacion.entidades.personal.herramienta import Herramienta

class TrabajadorService:
    """
    Servicio para gestionar la logica de negocio de los Trabajadores.
    
    Implementa US-015 (Asignar Apto Medico) y US-016 (Trabajar).
    """

    def asignar_apto_medico(self,
                              trabajador: Trabajador,
                              apto: bool,
                              fecha_emision: date,
                              observaciones: str | None = None) -> None:
        """
        Crea y asigna un AptoMedico a un trabajador.
        Implementacion de US-015.

        Args:
            trabajador (Trabajador): El trabajador a certificar.
            apto (bool): True si esta apto.
            fecha_emision (date): Fecha del certificado.
            observaciones (str | None, optional): Comentarios medicos.
        """
        print(f"\n--- Asignando Apto Medico a {trabajador.get_nombre()} ---")
        
        # 1. Crear la entidad AptoMedico
        apto_medico = AptoMedico(
            apto=apto,
            fecha_emision=fecha_emision,
            observaciones=observaciones
        )
        
        # 2. Asignarla al trabajador
        trabajador.set_apto_medico(apto_medico)
        
        if apto:
            print(f"Trabajador {trabajador.get_nombre()} ahora esta APTO.")
        else:
            print(f"Trabajador {trabajador.get_nombre()} ahora esta NO APTO.")

    @staticmethod
    def _obtener_id_tarea(tarea: Tarea) -> int:
        """
        Metodo helper estatico para el ordenamiento de tareas.
        
        Se usa en lugar de 'lambda' para cumplir con la
        Rubrica 3.4 y Rubrica Auto (QUAL-002).
        
        Args:
            tarea (Tarea): La tarea de la que se extrae el ID.

        Returns:
            int: El ID de la tarea.
        """
        return tarea.get_id_tarea()

    def trabajar(self,
                 trabajador: Trabajador,
                 fecha: date,
                 util: 'Herramienta') -> bool:
        """
        Ejecuta las tareas asignadas a un trabajador para una fecha dada.
        Implementacion de US-016.

        Args:
            trabajador (Trabajador): El trabajador que ejecutara las tareas.
            fecha (date): La fecha de las tareas a ejecutar.
            util (Herramienta): La herramienta a utilizar.

        Returns:
            bool: True si pudo trabajar, False si no tenia apto medico.
        """
        print(f"\n--- {trabajador.get_nombre()} intenta trabajar (Fecha: {fecha}) ---")
        
        # 1. Validacion de Apto Medico (Criterio de Aceptacion US-016)
        apto = trabajador.get_apto_medico()
        if apto is None or not apto.esta_apto():
            print(f"ERROR: {trabajador.get_nombre()} no puede trabajar. "
                  f"No tiene Apto Medico vigente.")
            return False # No puede trabajar

        # 2. Obtener todas las tareas
        todas_las_tareas = trabajador.get_tareas()
        
        # 3. Filtrar tareas por fecha y estado
        tareas_para_hoy = [
            t for t in todas_las_tareas
            if t.get_fecha() == fecha and t.get_estado() == EstadoTarea.PENDIENTE
        ]

        if not tareas_para_hoy:
            print(f"{trabajador.get_nombre()} no tiene tareas pendientes para hoy.")
            return True # Pudo "trabajar" (no hacer nada)

        # 4. Ordenar por ID descendente (Criterio US-016)
        #    Usamos el metodo estatico en 'key' para evitar lambda
        tareas_para_hoy.sort(key=self._obtener_id_tarea, reverse=True)

        # 5. Ejecutar tareas
        print(f"{trabajador.get_nombre()} comienza sus tareas con: {util.get_nombre()}")
        for tarea in tareas_para_hoy:
            print(f"  -> Ejecutando tarea {tarea.get_id_tarea()}: {tarea.get_descripcion()}")
            tarea.completar_tarea() # Marcar como completada
            
        print(f"Tareas de {trabajador.get_nombre()} completadas.")
        return True # Trabajo exitoso