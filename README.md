# Analizador Genético Web

Este proyecto es una aplicación web de análisis de variantes genéticas en formato VCF para la identificación de variantes con significancia patogénica o no patogénica. Utilizando un backend rápido y eficiente con FastAPI y un frontend limpio con tecnologías estandar (HTML, CSS y JavaScript).

## Características Principales

* **Procesamiento de archivos:** Subida y validación de archivos en formato VCF directamente desde el explorador del sistema.
* **Consulta de APIs:** Integración con el servicio externo **Myvariant.info** para la consulta de variantes con relevancia clínica.
* **Procesamiento de variantes:** Filtrado de la información otorgada por la API para mostrar si una variante es patogénica o benigna.
* **Opciones de consulta flexible:** Posibilidad de analizar archivos o introducir datos manualmente para consultar una variante de manera individual.
* **Interfaz limpia:** Diseño interactivo, responsivo y fácil de usar, con separación total de responsabilidades (HTML, CSS y JS independientes).
* **Arquitectura estructurada:** Organización del proyecto basada en los estándares de FastAPI.

## Tecnologías Utilizadas

* **Backend:** Python 3.14, FastAPI, Uvicorn
* **Librerías Python:** Requests (para consumo de APIs)
* **Frontend:** HTML5, CSS3, JavaScript

# Instalación y Configuración
El proyecto ha sido desarrollado y probado en entornos GNU/Linux (Ubuntu) utilizando el entorno de ejecución de Python 3.14.

Sigue estos pasos para configurar el proyecto:

1. Clonar el repositorio:
```bash
git clone [https://github.com/Irving326/analizador_genetico.git](https://github.com/Irving326/analizador_genetico.git)
cd analizador_genetico
```

2. Crear entorno virtual:
```bash
python3 -m venv .venv
```

3. Activar entorno virtual:
```bash
source .venv/bin/activate
```

4. Instalar requirements.txt:
``` bash
pip install -r requirements.txt
```

5. Ejecutar el entorno de desarrollo uvicorn:
``` bash
uvicorn app.main:app --reload
```

6. Una vez en el servidor abrir un navegador y dirigirse a:
http://127.0.0.1:8000
