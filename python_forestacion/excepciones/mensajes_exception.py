"""
Modulo centralizado para los mensajes de error del sistema.
"""

# --- Mensajes de Excepciones de Dominio ---

# AguaAgotadaException
TEC_AGUA_AGOTADA = "Agua disponible ({}) es menor que la requerida ({})"
USR_AGUA_AGOTADA = "No hay suficiente agua en la plantacion para regar."

# SuperficieInsuficienteException
TEC_SUPERFICIE_INSUFICIENTE = "Superficie disponible ({}) es menor que la requerida ({})"
USR_SUPERFICIE_INSUFICIENTE = "No hay suficiente espacio en la plantacion."

# --- Mensajes de Excepciones de Persistencia ---

# Leer
TEC_LEER_NO_EXISTE = "IOError: Archivo no encontrado en {}"
USR_LEER_NO_EXISTE = "Error de lectura: El archivo no existe."
TEC_LEER_CORRUPTO = "PickleError / EOFError: El archivo {} esta corrupto o vacio."
USR_LEER_CORRUPTO = "Error de lectura: El archivo parece estar corrupto."
TEC_LEER_OTRO = "Exception: Error desconocido al leer el archivo {}."
USR_LEER_OTRO = "Error de lectura: Ocurrio un problema desconocido."

# Escribir
TEC_ESCRIBIR_IO = "IOError: No se pudo escribir en el directorio {}"
USR_ESCRIBIR_IO = "Error de escritura: No se tienen permisos o el directorio no existe."
TEC_ESCRIBIR_PICKLE = "PickleError: Error al serializar el objeto {}."
USR_ESCRIBIR_PICKLE = "Error de escritura: No se pudo guardar el registro."
TEC_ESCRIBIR_OTRO = "Exception: Error desconocido al escribir el archivo {}."
USR_ESCRIBIR_OTRO = "Error de escritura: Ocurrio un problema desconocido."