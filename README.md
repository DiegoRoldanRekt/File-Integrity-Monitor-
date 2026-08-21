# 🛡️ File Integrity Monitor

> **Sistema de monitoreo de integridad de archivos desarrollado en Python.**

---

## 🧰 Tecnologías

- 🐍 **Python**
- `hashlib` — Generación de hashes SHA-256
- `json` — Almacenamiento de la línea base de hashes
- `os` — Gestión y recorrido de archivos y directorios
- `datetime` — Registro de fecha y hora de eventos
- `argparse` — Gestión de argumentos desde la terminal

---

## ⚙️ Funcionalidades

- 🔐 **Generación de hashes SHA-256**
- ✏️ **Detección de archivos modificados**
- ➕ **Detección de archivos nuevos**
- 🗑️ **Detección de archivos eliminados**
- 📝 **Sistema de logging**
- ⚠️ **Manejo de errores**
- 💾 **Persistencia de la línea base mediante JSON**
- 📊 **Resumen de eventos detectados**

---

## 🔍 ¿Cómo funciona?

El programa genera una **huella digital SHA-256** para cada archivo de la carpeta monitoreada.

Estos hashes se almacenan como una línea base:

```text
Archivo → SHA-256

Cómo ejecutar (En bash):
1era forma ---- python proyecto.py archivos 
2nda forma ---- python proyecto.py "C:\Users\User\Desktop\Documentos"
y para ver ayuda python proyecto.py --help


