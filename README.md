# fee-receipt-extractor
Extractor de boletas de honorarios (PDF → Excel) en Python.
# Fee Receipt Extractor

Proyecto para preparar una herramienta de extracción de información desde boletas en formato PDF.

## Requisitos

- Python 3 instalado.
- Git instalado.

## Instalación

Clona el repositorio y entra en su carpeta:

```bash
git clone https://github.com/byz-asesores/fee-receipt-extractor.git
cd fee-receipt-extractor
```

Crea y activa el entorno virtual.

En Windows con PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Ejecuta el programa desde la carpeta principal:

```bash
python src/main.py
```

El programa muestra el mensaje `Extractor de boletas`.

## Dependencias

Las dependencias de Python se encuentran registradas en `requirements.txt`.
