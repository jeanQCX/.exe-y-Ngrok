# 🧪 Experimento: Generador QR

## 📖 Bitácora del Proyecto

Este repositorio nace como un ejercicio práctico y experimental. El origen fue una frustración común: necesitar un código QR rápido y tener que lidiar con páginas web de terceros llenas de anuncios, registros y flujos tediosos. 

Para resolverlo, primero programé un script local en Python (`generar_qr_gui.py`) usando Tkinter. Funcionaba perfecto, pero me llevó a preguntarme: **¿Qué tan difícil es convertir este script en un "programa de verdad" (con su `.exe` e ícono) o en mi propia página web?**

Este documento registra el aprendizaje al explorar dos formas o arquitecturas de despliegue distintas para un mismo problema: **El modelo Standalone (Ejecutable)** y **El modelo Cliente-Servidor (Web App)**.

---

## ⚖️ Comparativa de Arquitecturas: El Dilema

Antes de tocar el código, esta es la teoría de lo que estamos construyendo:

| Característica | 🖥️ Ruta 1: Desktop (.exe) | 🌐 Ruta 2: Web (Cliente-Servidor) |
| :--- | :--- | :--- |
| **Arquitectura** | Standalone / Thick Client (Cliente pesado). | Cliente - Servidor / Arquitectura Distribuida. |
| **Procesamiento** | 100% ocurre en la máquina del usuario. | El cálculo ocurre en el Servidor; el Cliente solo ve la interfaz. |
| **Interfaz (GUI)** | Librerías nativas del SO (Tkinter). | Tecnologías Web estándar (HTML, CSS, JS). |
| **Multiplataforma** | ❌ No. Un `.exe` de Windows no abre en celulares o Mac. | ✅ Sí. Solo requiere un navegador web. |
| **Privacidad / Red** | 100% Offline y privado. | Depende de la conexión al servidor. |

---

## 🛠️ Paso 0: Entorno Virtual e Instalación de Librerías

Para que este experimento funcione, no debemos ensuciar el Python global del sistema. Todo se hace en un entorno aislado (`venv`).

**1. Crear y activar el entorno (En Windows):**
```cmd
python -m venv venv
venv\Scripts\activate
```
*(Si PowerShell lanza un error de scripts, ejecuta: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`)*

**2. Instalar todas las dependencias del experimento:**
```cmd
pip install qrcode[pil] flask pyinstaller
```
*   `qrcode[pil]`: La lógica central (incluye Pillow para manejar la imagen).
*   `flask`: Para la Ruta 2 (Servidor Web).
*   `pyinstaller`: Para la Ruta 1 (Empaquetado del .exe).

---

## 🛤️ Ruta 1: El Ejecutable de Escritorio (.exe)

Partimos del script base `generar_qr_gui.py`. El objetivo es tener un programa autónomo que se abra con doble clic sin necesidad de abrir la consola ni instalar Python.

### Detalles Técnicos:
*   **El Ícono (`.ico`):** Para darle identidad, usamos un archivo `.ico`. No es una simple imagen, es un contenedor que guarda múltiples resoluciones (16x16, 32x32, etc.) para que Windows decida cuál usar en la barra de tareas o el escritorio sin pixelarlo.
*   **La Compilación:** Usamos PyInstaller. Con el `venv` activado, ejecutamos:

```cmd
pyinstaller --onefile --windowed --icon=qr_page_icon.ico generar_qr_gui.py
```

*   `--onefile`: Empaqueta Python, Tkinter y nuestro código en un solo archivo autoextraíble.
*   `--windowed`: Oculta la terminal negra de CMD de fondo.

**Resultado:** El programa final listo para usar y compartir queda en la carpeta `dist/`.

---

## 🛤️ Ruta 2: Arquitectura Cliente-Servidor (Web App)

El objetivo aquí es distinto: usar mi PC como servidor para que cualquiera pueda generar un QR desde su celular.

### Fase A: El Servidor Local (Solo en tu PC)
Al usar **Flask**, reestructuramos el código. Flask se encarga de la lógica (generar el QR en memoria RAM y pasarlo a base64) y se apoya en HTML/CSS para la interfaz visual.
Al ejecutar `python app.py`, el servidor se enciende en `http://localhost:5000`. 
**Ojo:** En este punto, la aplicación es estrictamente local. Nadie fuera de mi computadora puede acceder a ella.

*   *El truco del Favicon y la Caché:* Si agregas un `.ico` a tu web y luego lo cambias, a veces darle F5 no actualiza la imagen. Esto es por la memoria caché agresiva del navegador. **Solución:** Usar `Ctrl + F5` (o `Shift + F5`) para forzar una recarga profunda ("Hard Reload").

### Fase B: Exponiendo el servidor a Internet (Ngrok)
Para romper la barrera del "localhost" sin tener que lidiar con configuraciones complicadas de router o IPs públicas, la solución es usar un túnel inverso: **Ngrok**.

**Pasos para usar Ngrok:**
1.  Ir a la página oficial de [Ngrok](https://ngrok.com/) y crear una cuenta gratuita.
2.  Seguir las instrucciones en su panel para iniciar tu autenticación.
3.  Con tu servidor Flask corriendo en una terminal, abres otra terminal y ejecutas:
    ```cmd
    ngrok http 5000
    ```

**¿Qué pasa ahora?** Ngrok te da un enlace público (ej. `https://algo.ngrok-free.app`). Cuando alguien entra ahí desde su celular, Ngrok empuja esa visita de forma segura hacia el puerto 5000 de tu computadora. ¡Ya está en internet!

### ℹ️ Limitaciones del Plan Gratuito de Ngrok:
*   **1 solo túnel a la vez:** No puedes exponer varios puertos locales simultáneamente.
*   **Dominio Estático:** Ngrok ahora permite reclamar 1 dominio estático gratis (para que el link no cambie cada vez que cierras el programa).
*   **Pantalla de advertencia:** Al ser un link gratuito, la primera vez que un usuario entra, verá una pantalla de Ngrok pidiendo confirmar que confían en el sitio (para evitar phishing).
*   **Dependencia de tu PC:** Si apagas tu computadora o cierras la terminal, la página web se cae instantáneamente.
