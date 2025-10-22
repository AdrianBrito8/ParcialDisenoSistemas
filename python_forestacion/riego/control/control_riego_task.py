"""
Modulo del Controlador de Riego (Thread).
"""
import threading
import time
from typing import TYPE_CHECKING

# --- Imports de Servicios ---
from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService

# --- Imports de Entidades ---
from python_forestacion.entidades.terrenos.plantacion import Plantacion

# --- Imports de Excepciones ---
from python_forestacion.excepciones.agua_agotada_exception import AguaAgotadaException

# --- Imports de Constantes ---
from python_forestacion import constantes as C

# --- Imports para Type Hints ---
if TYPE_CHECKING:
    from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
    from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask


class ControlRiegoTask(threading.Thread):
    """
    Controlador de Riego Automatico.
    
    1.  Como Thread (US-012): Se ejecuta en un hilo daemon
        separado, evaluando las condiciones ambientales
        cada N segundos.
        
    2.  Recibe los sensores y servicios por Inyeccion de
        Dependencias.
        
    3.  Implementa la logica de decision para el riego.
    """
    
    def __init__(self,
                 sensor_temperatura: 'TemperaturaReaderTask',
                 sensor_humedad: 'HumedadReaderTask',
                 plantacion: Plantacion,
                 plantacion_service: PlantacionService):
        """
        Inicializa el Controlador.
        
        Configura el thread como 'daemon' (Rubrica 5.1).

        Args:
            sensor_temperatura (TemperaturaReaderTask): Instancia del sensor.
            sensor_humedad (HumedadReaderTask): Instancia del sensor.
            plantacion (Plantacion): La plantacion a regar.
            plantacion_service (PlantacionService): El servicio para regar.
        """
        # 1. Inicializar el Thread
        super().__init__(daemon=True, name="ControlRiegoThread")
        
        # 2. Inyeccion de Dependencias
        self._sensor_temp = sensor_temperatura
        self._sensor_hum = sensor_humedad
        self._plantacion = plantacion
        self._plantacion_service = plantacion_service
        
        # 3. Control de detencion (Graceful Shutdown - US-013)
        self._detenido: threading.Event = threading.Event()
        
    def _evaluar_condiciones(self) -> bool:
        """
        Evalua si las condiciones para el riego se cumplen.
        Logica de negocio de US-012.
        
        Usa el metodo PULL (get_ultima_lectura) de los sensores.
        """
        # 1. Obtener lecturas (PULL)
        temp = self._sensor_temp.get_ultima_lectura()
        hum = self._sensor_hum.get_ultima_lectura()
        
        # 2. Logica de decision (US-012)
        temp_ok = C.TEMP_MIN_RIEGO <= temp <= C.TEMP_MAX_RIEGO
        hum_ok = hum < C.HUMEDAD_MAX_RIEGO
        
        print(f"[{self.name}] Evaluando... "
              f"Temp: {temp:.1f}°C (OK: {temp_ok}), "
              f"Hum: {hum:.1f}% (OK: {hum_ok})")
              
        return temp_ok and hum_ok

    def run(self) -> None:
        """
        Metodo principal del Thread.
        Se ejecuta al llamar a .start()
        """
        print(f"[{self.name}] Iniciando control de riego automatico...")
        while not self._detenido.is_set():
            
            # 1. Evaluar si regar
            if self._evaluar_condiciones():
                
                # 2. Intentar regar
                try:
                    print(f"[{self.name}] CONDICIONES OPTIMAS. Iniciando riego...")
                    self._plantacion_service.regar(self._plantacion)
                    print(f"[{self.name}] Riego finalizado.")
                    
                except AguaAgotadaException as e:
                    # Manejo de excepcion (US-012)
                    print(f"[{self.name}] ERROR DE RIEGO: {e.get_user_message()}")
                    # No re-lanzamos, solo logueamos y continuamos.
                
            else:
                print(f"[{self.name}] Condiciones no optimas. No se riega.")

            # 3. Esperar
            self._detenido.wait(timeout=C.INTERVALO_CONTROL_RIEGO)
                
        print(f"[{self.name}] Control de riego detenido.")

    def detener(self) -> None:
        """
        Solicita la detencion del thread de forma segura.
        (US-013)
        """
        print(f"[{self.name}] Solicitando detencion de control...")
        self._detenido.set()