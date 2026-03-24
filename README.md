
# 🚗 sinfreno - Parking Management System 

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![UI: Tkinter](https://img.shields.io/badge/UI-Tkinter-orange)](https://docs.python.org/3/library/tkinter.html)

**CocheraInterfaz** es una solución integral para la gestión operativa de estacionamientos multi-torre. El sistema permite el control total sobre el ciclo de vida de un vehículo dentro del establecimiento: desde el ingreso alfanumérico validado hasta el cálculo complejo de tarifas con descuentos dinámicos y análisis de horas pico.

---

## 📖 Vista de Negocio (Business Overview)

En el mercado actual, la eficiencia en la rotación de vehículos y la precisión en el cobro son críticas. Este sistema está diseñado para:
- **Optimizar la rentabilidad:** Aplicando tarifas por hora configurables al inicio de la jornada.
- **Fidelización:** Implementación de políticas de descuento automáticas (ej. 15% de descuento en la Torre 3).
- **Inteligencia Operativa:** Identificación de "Horas Pico" para la asignación de personal y recursos.
- **Mantenimiento Dinámico:** Funcionalidad de "limpieza" de torres para liberar espacios tras cierres de turno.

---

## 🚀 Tecnologías Utilizadas

El proyecto se basa en una arquitectura limpia, separando la lógica de negocio de la interfaz de usuario:

- **Lenguaje:** Python 3.x
- **GUI:** `tkinter` & `ttk` (Temas avanzados para tablas y pestañas).
- **Manejo de Tiempo:** Librería `datetime` para cálculos de precisión de milisegundos en estadías.
- **Estructura de Datos (TADs):** Implementación personalizada de Tipos de Datos Abstractos:
  - **TAD Autos:** Encapsulamiento de la entidad vehículo.
  - **TAD Cochera:** Gestión de colecciones dinámicas de vehículos.
  - **TAD Cola:** Gestión FIFO (First-In-First-Out) para la organización de salida por torres.

---

## 🛠️ Arquitectura y Procedimientos

El sistema opera bajo un flujo de trabajo validado en cada etapa:

### 1. Inicialización
Al iniciar, el administrador define el **monto por hora** y la **cantidad de torres**. El sistema carga automáticamente un set de datos de prueba (`autosPredefinidos`) para facilitar el testing de integración.

### 2. Gestión de Vehículos
- **Registro Alfanumérico:** Validación estricta de patentes (debe contener letras y números).
- **Modificación en Caliente:** Permite corregir errores de ingreso (torre o patente) sin interrumpir el cronómetro de estadía.
- **Salida y Cobro:** Cálculo automático basado en la diferencia temporal. 
  - *Fórmula:* `(HoraSalida - HoraEntrada) * TarifaBase * (0.85 si Torre == 3)`.

### 3. Análisis y Reportes
- **Recaudación por Torre:** Desglose financiero detallado.
- **Análisis de Hora Pico:** Filtro estadístico que identifica vehículos ingresados de 07:00-10:00 y 18:00-21:00.
- **Gestión de Colas:** Visualización ordenada de la secuencia de vehículos por torre para optimizar la logística de egreso.

---

## 📦 Estructura del Proyecto

```bash
├── assets/
│   └── icons/              # Recursos visuales (iconos de vehículos)
├── tads/                   # Capa de lógica y estructuras de datos
│   ├── tadAutos.py         # Definición del objeto Auto
│   ├── tadCochera.py       # Gestión de la lista de la cochera
│   ├── tadColaAux.py       # Operaciones auxiliares de colas
│   └── tadColaTorres.py    # Lógica de colas específica por torre
└── cocheraInterfaz.py      # Controlador principal e Interfaz Gráfica
```

---

## 🚦 Estado Actual del Proyecto

El sistema se encuentra en una fase de **Estabilidad Funcional**. 
- [x] CRUD completo de vehículos.
- [x] Lógica de descuentos por torre.
- [x] Interfaz multiventana con validación de errores.
- [x] Simulación de "Modo Prueba" para limpieza de torres pasadas las 18hs.

---

## 🛣️ Roadmap (Puntos a Mejorar)

Para llevar este proyecto a un nivel empresarial, se planean las siguientes mejoras:

1. **Persistencia de Datos:** Migrar de listas en memoria a una base de datos SQL (SQLite/PostgreSQL) para evitar la pérdida de datos al cerrar el programa.
2. **Generación de Comprobantes:** Integración con librerías de PDF (como `ReportLab`) para emitir tickets de cobro.
3. **Módulo de Usuarios:** Implementar login con diferentes niveles de acceso (Admin vs. Operador).
4. **Dashboard Visual:** Reemplazar las tablas simples por gráficos de barras (Matplotlib) para la recaudación.
5. **API de Integración:** Crear un endpoint para que los clientes puedan consultar la disponibilidad de torres desde una App móvil.

---

## 🔧 Instalación y Ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/cochera-interfaz.git
   ```
2. Asegurarse de tener Python instalado:
   ```bash
   python --version
   ```
3. Ejecutar la aplicación:
   ```bash
   python cocheraInterfaz.py
   ```

---

## 🤝 Contribuciones

Las contribuciones son lo que hacen que la comunidad de código abierto sea un lugar increíble para aprender, inspirar y crear. Cualquier contribución que hagas será **muy apreciada**.

1. Realiza un Fork del proyecto.
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`).
3. Haz un Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`).
4. Empuja la rama (`git push origin feature/AmazingFeature`).
5. Abre un Pull Request.

---

**Desarrollado para la gestión eficiente de espacios urbanos.** 🚗💨
