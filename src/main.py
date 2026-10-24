print("Extractor de boletas")

import pdfplumber


def leer_texto(ruta):
    """Lee y devuelve el texto completo de un archivo PDF."""
    texto_completo = ""

    with pdfplumber.open(ruta) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()

            if texto:
                texto_completo += texto + "\n"

    return texto_completo


if __name__ == "__main__":
    ruta =  "src/data/PRUEBA_boleta_ficticia_1001.pdf"  
    texto = leer_texto(ruta)
    print(texto)


import re
import pdfplumber


def leer_texto(ruta):
    """Lee y devuelve el texto completo de un archivo PDF."""
    texto_completo = ""

    with pdfplumber.open(ruta) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()

            if texto:
                texto_completo += texto + "\n"

    return texto_completo


def convertir_monto(monto):
    """Convierte un importe chileno, como $450.000, en un número."""
    if monto is None:
        return None

    monto_limpio = monto.replace("$", "").replace(".", "")
    monto_limpio = monto_limpio.replace(" ", "")

    return int(monto_limpio)


def extraer_datos(texto):
    """Prepara los campos que se extraerán de una boleta."""
    datos = {
        "numero": None,
        "fecha": None,
        "emisor": None,
        "rut_emisor": None,
        "receptor": None,
        "rut_receptor": None,
        "monto_bruto": None,
        "retencion": None,
        "monto_liquido": None,
    }

    # Aquí añadiremos las reglas para identificar
    # cada campo según el texto real de las boletas.

    return datos


if __name__ == "__main__": 
    carpeta_proyecto = Path(__file__).resolve().parent.parent 
    ruta = carpeta_proyecto / "src" / "data" / "PRUEBA_boleta_ficticia_1001.pdf"

    print("Archivo que se intentará abrir:", ruta)
    print("¿Existe el archivo?", ruta.exists())

    texto = leer_texto(str(ruta))

    print("\nTexto de la boleta:")
    print(texto)

    datos = extraer_datos(texto)

    print("\nDatos extraídos:")
    print(datos) 



    import re
from pathlib import Path

import pdfplumber


def leer_texto(ruta):
    """Lee y devuelve el texto completo de un archivo PDF."""
    texto_completo = ""

    with pdfplumber.open(ruta) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"

    return texto_completo


def convertir_monto(monto):
    """Convierte un importe chileno, como 412.000, en un entero."""
    if monto is None:
        return None

    return int(monto.replace("$", "").replace(".", "").replace(" ", ""))


def extraer_datos(texto):
    """Extrae los datos principales de una boleta de honorarios."""
    datos = {
        "numero": None,
        "fecha": None,
        "emisor": None,
        "rut_emisor": None,
        "receptor": None,
        "rut_receptor": None,
        "monto_bruto": None,
        "retencion": None,
        "monto_liquido": None,
    }

    numero = re.search(r"N\s*[°º]\s*(\d+)", texto, re.IGNORECASE)
    if numero:
        datos["numero"] = numero.group(1)

    fecha = re.search(r"Fecha:\s*(.+)", texto, re.IGNORECASE)
    if fecha:
        datos["fecha"] = fecha.group(1).strip()

    emisor = re.search(
        r"\n([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ ]+)\s*\n\s*N\s*[°º]",
        texto,
    )
    if emisor:
        datos["emisor"] = emisor.group(1).strip()

    rut_emisor = re.search(r"RUT:\s*([\d.]+-[\dkK])", texto)
    if rut_emisor:
        datos["rut_emisor"] = rut_emisor.group(1)

    receptor = re.search(
        r"Señor\(es\):\s*(.*?)\s+Rut:\s*([\d.]+-[\dkK])",
        texto,
        re.IGNORECASE,
    )
    if receptor:
        datos["receptor"] = receptor.group(1).strip()
        datos["rut_receptor"] = receptor.group(2)

    bruto = re.search(
        r"Total de honorario\s*\$?\s*:\s*\$?\s*([\d.]+)",
        texto,
        re.IGNORECASE,
    )
    if bruto:
        datos["monto_bruto"] = convertir_monto(bruto.group(1))

    retencion = re.search(
        r"Impto\.\s*Retenido:\s*\$?\s*([\d.]+)",
        texto,
        re.IGNORECASE,
    )
    if retencion:
        datos["retencion"] = convertir_monto(retencion.group(1))

    liquido = re.search(r"Total:\s*\$?\s*([\d.]+)", texto)
    if liquido:
        datos["monto_liquido"] = convertir_monto(liquido.group(1))

    return datos


if __name__ == "__main__":
    ruta = Path(__file__).resolve().parent / "data" / "PRUEBA_boleta_ficticia_1001.pdf"

    print("Archivo:", ruta)
    print("¿Existe el archivo?", ruta.exists())

    texto = leer_texto(str(ruta))

    print("\nTexto de la boleta:")
    print(texto)

    datos = extraer_datos(texto)

    print("\nDatos extraídos:")
    print(datos)