# 🛠️ reports Service - Pruebas Unitarias

Este documento describe cómo ejecutar las pruebas unitarias y funcionales del servicio `reports-Service`.  

## 📌 **Índice**
1. [📦 Requisitos Previos](#requisitos-previos)
2. [🚀 Activar el Entorno Virtual](#activar-el-entorno-virtual)
3. [🔧 Configurar el `PYTHONPATH`](#configurar-el-pythonpath)
4. [🧪 Ejecutar las Pruebas](#ejecutar-las-pruebas)
   - [Ejecutar todas las pruebas](#ejecutar-todas-las-pruebas)
   - [Ejecutar una prueba específica](#ejecutar-una-prueba-específica)
   - [Ejecutar con más detalles](#ejecutar-con-más-detalles)
5. [🐛 Solución de Problemas](#solución-de-problemas)

---

## 📦 **Requisitos Previos**
Antes de ejecutar las pruebas, asegúrate de tener instalado lo siguiente:

- **Python 3.12.6** o una versión compatible.
- **pytest** instalado en tu entorno virtual:
  ```sh
  pip install pytest

# 🚀 activar-el-entorno-virtual

Para ejecutar las pruebas, primero debes activar el entorno virtual.

- **Windows - PowerShell**
    ```sh
      .\.venv\Scripts\Activate

- **Windows - PowerShell**
    ```sh
      .\.venv\Scripts\activate.bat
    ```
- **Mac/Linux**
    ```sh
      source .venv/bin/activate
    ```
# 🔧 Configurar el PYTHONPATH

Para que pytest reconozca correctamente el módulo src, establece PYTHONPATH antes de ejecutar las pruebas.

- **PowerShell:**
    ```sh
      $env:PYTHONPATH="D:\GITHUB\reports-Service"
    ```
- **cmd.exe:**
    ```sh
      set PYTHONPATH=D:\GITHUB\reports-Service
    ```

# 🧪 Ejecutar las Pruebas

- **Ejecutar todas las pruebas:**

    ```sh
      python -m pytest tests/pytest/tests_reports.py
    ```
- **Ejecutar una prueba específica:**

    ```sh
      python -m pytest tests/pytest/tests_reports.py -k test_delete_profile_by_id
    ```
# 🐛 Solución de Problemas

Si pytest no encuentra el módulo src, intenta las siguientes soluciones:

- **Ejecuta pytest con python -m pytest en lugar de solo pytest**

    ```sh
      python -m pytest tests/pytest/tests_reports.py
    ```
