"""
Modulo del Sensor de Temperatura (Thread y Observable).
"""
import threading
import time
import random
from typing_extensions import override

# --- Imports de Patrones ---
from python_forestacion.patrones.observer.observable import Observable

# --- Imports de Constantes ---
from python_forestacion import constantes as C

class TemperaturaReaderTask(threading.Thread, Observable[float]):
    """
    Sensor de Temperatura.
    
    1.  Como Thread (US-010): Se ejecuta en un hilo daemon separado
        leyendo temperatura cada N segundos.
    2.  Como Observable[float] (US-TECH-003): Notifica a sus
        observadores cada vez que tiene una nueva lectura.
    """
    
    def __init__(self):
        """
        Inicializa el sensor.
        
        Configura el thread como 'daemon' para que finalice
        automaticamente cuando el programa principal termine.
        (Rubrica 5.1)
        """
        # 1. Inicializar el Thread
        #    daemon=True es clave (Rubrica 5.1)
        super(threading.Thread, self).__init__(daemon=True, name="SensorTempThread")
        
        # 2. Inicializar el Observable
        super(Observable, self).__init__()
        
        # 3. Control de detencion (Graceful Shutdown - US-013)
        self._detenido: threading.Event = threading.Event()
        
        # 4. Almacenamiento de ultima lectura (para PULL)
        self._ultima_lectura: float = 20.0 # Un valor inicial default

    def _leer_temperatura(self) -> float:
        """Simula la lectura de un sensor fisico."""
        temp = random.uniform(C.SENSOR_TEMP_MIN, C.SENSOR_TEMP_MAX)
        return temp

    def run(self) -> None:
        """
        Metodo principal del Thread.
        Se ejecuta al llamar a .start()
        """
        print(f"[{self.name}] Iniciando sensor de temperatura...")
        while not self._detenido.is_set():
            # 1. Leer valor
            temperatura = self._leer_temperatura()
            
            # 2. Guardar valor (para PULL)
            self._ultima_lectura = temperatura
            
            # 3. Notificar (PUSH - Observer Pattern)
            # (Rubrica 1.3)
            self.notificar_observadores(temperatura)
            
            # 4. Esperar.
            #    Usa 'wait' en lugar de 'sleep' para que la
            #    detencion sea instantanea (si .detener() es llamada)
            self._detenido.wait(timeout=C.INTERVALO_SENSOR_TEMPERATURA)
                
        print(f"[{self.name}] Sensor de temperatura detenido.")

    def detener(self) -> None:
        """
        Solicita la detencion del thread de forma segura.
        (US-013)
        """
        print(f"[{self.name}] Solicitando detencion de sensor...")
        self._detenido.set()

    def get_ultima_lectura(self) -> float:
        """
        Permite al sistema (ControlRiegoTask) obtener
        la ultima lectura (metodo PULL).
        
        Returns:
            float: La ultima temperatura registrada.
        """
        return self._ultima_lectura