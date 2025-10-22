"""
Modulo Centralizado de Constantes del Sistema (PythonForestal)

Este archivo contiene todos los valores fijos (constantes o "magic numbers")
del sistema para cumplir con la rubrica de evaluacion (Seccion 3.4).

NO deben existir valores hardcodeados en los servicios o entidades.
"""

# ==============================================================================
# --- EPIC 2: GESTION DE CULTIVOS (US-004 a US-008) ---
# ==============================================================================

# --- Constantes de Pino (US-004) ---
SUPERFICIE_PINO: float = 2.0  # m²
AGUA_INICIAL_PINO: int = 2  # litros
ALTURA_INICIAL_ARBOL: float = 1.0  # metros

# --- Constantes de Olivo (US-005) ---
SUPERFICIE_OLIVO: float = 3.0  # m²
AGUA_INICIAL_OLIVO: int = 5  # litros
ALTURA_INICIAL_OLIVO: float = 0.5 # metros (especifico de US-005)

# --- Constantes de Lechuga (US-006) ---
SUPERFICIE_LECHUGA: float = 0.10  # m²
AGUA_INICIAL_LECHUGA: int = 1  # litros

# --- Constantes de Zanahoria (US-007) ---
SUPERFICIE_ZANAHORIA: float = 0.15  # m²
AGUA_INICIAL_ZANAHORIA: int = 0  # litros (sin agua inicial)

# --- Constantes de Riego (US-008) ---
AGUA_POR_RIEGO: int = 10  # Litros consumidos por la plantacion en cada riego

# --- Constantes de Estrategia de Absorcion (Strategy Pattern) (US-008) ---
# Estrategia Seasonal (Pino, Olivo)
ABSORCION_SEASONAL_VERANO: int = 5  # litros
ABSORCION_SEASONAL_INVIERNO: int = 2  # litros
MES_INICIO_VERANO: int = 3  # Marzo
MES_FIN_VERANO: int = 8   # Agosto

# Estrategia Constante (Lechuga, Zanahoria)
ABSORCION_CONSTANTE_LECHUGA: int = 1  # litros
ABSORCION_CONSTANTE_ZANAHORIA: int = 2  # litros

# --- Constantes de Crecimiento (US-008) ---
CRECIMIENTO_PINO_POR_RIEGO: float = 0.10  # metros
CRECIMIENTO_OLIVO_POR_RIEGO: float = 0.01  # metros


# ==============================================================================
# --- EPIC 3: RIEGO AUTOMATIZADO (US-010 a US-013) ---
# ==============================================================================

# --- Sensor de Temperatura (US-010) ---
INTERVALO_SENSOR_TEMPERATURA: float = 2.0  # segundos
SENSOR_TEMP_MIN: int = -25  # °C
SENSOR_TEMP_MAX: int = 50   # °C

# --- Sensor de Humedad (US-011) ---
INTERVALO_SENSOR_HUMEDAD: float = 3.0  # segundos
SENSOR_HUMEDAD_MIN: int = 0  # %
SENSOR_HUMEDAD_MAX: int = 100  # %

# --- Control de Riego (US-012) ---
INTERVALO_CONTROL_RIEGO: float = 2.5  # segundos
TEMP_MIN_RIEGO: int = 8  # °C
TEMP_MAX_RIEGO: int = 15  # °C
HUMEDAD_MAX_RIEGO: int = 50  # %

# --- Control de Threads (US-013) ---
THREAD_JOIN_TIMEOUT: float = 2.0  # segundos


# ==============================================================================
# --- EPIC 6: PERSISTENCIA (US-021) ---
# ==============================================================================

DIRECTORIO_DATA: str = "data"
EXTENSION_DATA: str = ".dat"