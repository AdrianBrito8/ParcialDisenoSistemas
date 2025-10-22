# 🌲 Sistema de Gestión Forestal (PythonForestal)
### Parcial - Diseño de Sistemas

Este proyecto implementa un **sistema de gestión para fincas forestales y agrícolas**, desarrollado como parte del **Parcial de Diseño de Sistemas**.  
El objetivo principal es **aplicar patrones de diseño de software** para crear una solución **modular, mantenible y robusta**.

---

## ✨ Características Principales

El sistema simula las siguientes funcionalidades clave, basadas en las [Historias de Usuario](./USER_STORIES.md):

- **Gestión de Fincas:** Creación de terrenos, plantaciones y registros forestales.  
- **Gestión de Cultivos:** Soporte para cuatro tipos de cultivos (`Pino`, `Olivo`, `Lechuga`, `Zanahoria`) con características específicas.  
- **Riego Automatizado:** Sistema concurrente con sensores de temperatura y humedad que controlan el riego en tiempo real.  
- **Gestión de Personal:** Registro de trabajadores, asignación de tareas y validación de apto médico.  
- **Operaciones de Negocio:** Gestión centralizada de múltiples fincas, fumigación y cosecha por tipo de cultivo.  
- **Persistencia:** Guardado y lectura de registros forestales en disco utilizando **Pickle**.

---

## 🧩 Patrones de Diseño Implementados

Este proyecto demuestra la aplicación práctica de varios **patrones de diseño**, según la [Rúbrica de Evaluación](./RUBRICA_EVALUACION.md):

1. **Singleton (Thread-Safe):**  
   Utilizado en `CultivoServiceRegistry` para garantizar una única instancia del registro de servicios, con manejo seguro de concurrencia (`threading.Lock`).

2. **Factory Method:**  
   Implementado en `CultivoFactory` para la creación desacoplada de las distintas clases de `Cultivo`.

3. **Observer:**  
   Aplicado en el sistema de riego (`sensores` como `Observable[float]`) para notificar cambios ambientales.  
   *Nota:* el controlador (`ControlRiegoTask`) implementa un enfoque *PULL* por claridad.

4. **Strategy:**  
   Define algoritmos intercambiables de absorción de agua (`AbsorcionAguaStrategy`) con implementaciones `Seasonal` y `Constante`, inyectadas en los servicios de cultivo.

5. **Registry:**  
   Usado en `CultivoServiceRegistry` para el despacho polimórfico de operaciones, eliminando la necesidad de usar `isinstance()`.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x  
- **Bibliotecas:** Solo se utilizan módulos de la **biblioteca estándar** (`os`, `sys`, `datetime`, `threading`, `pickle`, `abc`, `typing`, `enum`, `random`).  
  → *No requiere instalación de dependencias externas.*

---

## 📁 Estructura del Proyecto

El código está organizado siguiendo principios de **separación de responsabilidades**:

```
ParcialDisenoSistemas/
├── python_forestacion/            # Paquete principal del código fuente
│   ├── constantes.py              # Constantes centralizadas (NO Magic Numbers)
│   ├── entidades/                 # Clases de datos (Modelo de Dominio)
│   │   ├── cultivos/
│   │   ├── personal/
│   │   └── terrenos/
│   ├── excepciones/               # Excepciones personalizadas
│   ├── patrones/                  # Implementaciones de patrones de diseño
│   │   ├── factory/
│   │   ├── observer/
│   │   ├── singleton/             # (Implementado en Registry)
│   │   └── strategy/
│   ├── riego/                     # Lógica del sistema de riego (Threads)
│   │   ├── control/
│   │   └── sensores/
│   └── servicios/                 # Lógica de negocio (Service Layer)
│       ├── cultivos/              # (Incluye el Registry/Singleton)
│       ├── negocio/
│       ├── personal/
│       └── terrenos/
├── .gitignore                     # Ignora archivos generados y de entorno
├── buscar_paquete.py              # Script de integración (provisto por la cátedra)
├── main.py                        # Script principal de ejecución
├── README.md                      # Este archivo
├── README_BUSCAR_PAQUETE.md       # Documentación del script de integración
├── RUBRICA_AUTOMATIZADA.md        # Criterios de corrección automática
├── RUBRICA_EVALUACION.md          # Rúbrica de evaluación detallada
└── USER_STORIES.md                # Requisitos funcionales
```

---

## 🚀 Cómo Ejecutar

### 1. Ejecutar la Simulación Principal

Ejecuta el flujo completo definido en `main.py`, demostrando todas las funcionalidades y patrones:

```bash
python3 main.py
```

Al finalizar, el sistema mostrará el mensaje:

```
--- EJEMPLO COMPLETADO EXITOSAMENTE ---
```

y se habrá creado la carpeta `data/` con un archivo `.dat`.

---

### 2. Generar el Archivo Integrador (para la corrección)

El siguiente comando utiliza el script `buscar_paquete.py` (provisto por la cátedra) para consolidar todo el código en un único archivo `integradorFinal.py`:

```bash
python3 buscar_paquete.py integrar python_forestacion
```

> **Nota:**  
> Los archivos `integrador.py` e `integradorFinal.py` están incluidos en `.gitignore` y no deben subirse al repositorio.

---

## 👨‍💻 Autor

**Adrián Brito**  
Universidad de Mendoza – Ingeniería en Informática  
Parcial de la asignatura **Diseño de Sistemas**
