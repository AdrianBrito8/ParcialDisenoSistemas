"""
Modulo del Sensor de Humedad (Thread y Observable).
"""
import threading
import time
import random
from typing_extensions import override

# --- Imports de Patrones ---
from python_forestacion.patrones.observer.observable import Observable

# --- Imports de Constantes ---
from python_forestacion import constantes as C

class HumedadReaderTask(threading.Thread, Observable[float]):
    """
    Sensor de Humedad.
    
    1.  Como Thread (US-011): Se ejecuta en un hilo daemon separado
        leyendo humedad cada N segundos.
    2.  Como Observable[float] (US-TECH-003): Notifica a sus
        observadores cada vez que tiene una nueva lectura.
    """
    
    def __init__(self):
        """
        Inicializa el sensor.
        
        Configura el thread como 'daemon' (Rubrica 5.1)
        """
        # --- CORRECCION AQUI ---
        # Llamamos a los __init__ de CADA padre explícitamente
        # para evitar el conflicto de 'super()' en herencia multiple.

        # 1. Inicializar el Thread EXPLICITAMENTE
        threading.Thread.__init__(self, daemon=True, name="SensorHumedThread")
        
        # 2. Inicializar el Observable EXPLICITAMENTE
        Observable.__init__(self)
        
        # 3. Control de detencion (Graceful Shutdown - US-013)
        self._detenido: threading.Event = threading.Event()
        
        # 4. Almacenamiento de ultima lectura (para PULL)
        self._ultima_lectura: float = 60.0 # Un valor inicial default

    def _leer_humedad(self) -> float:
        """Simula la lectura de un sensor fisico."""
        humedad = random.uniform(C.SENSOR_HUMEDAD_MIN, C.SENSOR_HUMEDAD_MAX)
        return humedad

    def run(self) -> None:
        """
        Metodo principal del Thread.
        Se ejecuta al llamar a .start()
        """
        print(f"[{self.name}] Iniciando sensor de humedad...")
        while not self._detenido.is_set():
            # 1. Leer valor
            humedad = self._leer_humedad()
            
            # 2. Guardar valor (para PULL)
            self._ultima_lectura = humedad
            
            # 3. Notificar (PUSH - Observer Pattern)
            self.notificar_observadores(humedad)
            
            # 4. Esperar
            self._detenido.wait(timeout=C.INTERVALO_SENSOR_HUMEDAD)
                
        print(f"[{self.name}] Sensor de humedad detenido.")

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
            float: La ultima humedad registrada.
        """
        return self._ultima_lectura