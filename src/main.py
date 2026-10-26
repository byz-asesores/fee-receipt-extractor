
import re
from pathlib import Path

import pandas as pd
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
    """Convierte un monto chileno, como 412.000, en un entero."""
    if not monto:
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

    numero = re.search(r"\bN\s*[°º]\s*(\d+)", texto, re.IGNORECASE)
    if numero:
        datos["numero"] = numero.group(1)

    fecha = re.search(r"Fecha:\s*([^\r\n]+)", texto, re.IGNORECASE)
    if fecha:
        datos["fecha"] = fecha.group(1).strip()

    emisor = re.search(
        r"BOLETA DE HONORARIOS\s*\r?\n"
        r"\s*\(FICTICIA\)\s*\r?\n"
        r"\s*([^\r\n]+)\s*\r?\n"
        r"\s*N\s*[°º]\s*\d+",
        texto,
        re.IGNORECASE,
    )
    if not emisor:
        emisor = re.search(
            r"BOLETA DE HONORARIOS\s*\r?\n"
            r"\s*([^\r\n]+)\s*\r?\n"
            r"\s*N\s*[°º]\s*\d+",
            texto,
            re.IGNORECASE,
        )
    if emisor:
        datos["emisor"] = emisor.group(1).strip()

    rut_emisor = re.search(
        r"RUT:\s*([\d.]+-[\dkK])", texto, re.IGNORECASE
    )
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

    liquido = re.search(r"Total:\s*\$?\s*([\d.]+)", texto, re.IGNORECASE)
    if liquido:
        datos["monto_liquido"] = convertir_monto(liquido.group(1))

    return datos


def procesar_carpeta(carpeta_pdf, archivo_excel):
    """Procesa todos los PDF de la carpeta y genera un Excel."""
    archivos_pdf = sorted(carpeta_pdf.glob("*.pdf"))

    if not archivos_pdf:
        print(f"No se encontraron PDF en: {carpeta_pdf}")
        return

    resultados = []

    for ruta_pdf in archivos_pdf:
        print(f"Procesando: {ruta_pdf.name}")

        try:
            texto = leer_texto(ruta_pdf)
            datos = extraer_datos(texto)
            datos["archivo"] = ruta_pdf.name

            campos_clave = (
                "numero", "fecha", "emisor", "rut_emisor",
                "receptor", "rut_receptor", "monto_bruto",
                "retencion", "monto_liquido",
            )
            encontrados = sum(
                datos[campo] is not None for campo in campos_clave
            )
            datos["estado"] = (
                "OK" if encontrados == len(campos_clave)
                else f"Incompleto: {encontrados}/{len(campos_clave)} campos"
            )

            resultados.append(datos)

        except Exception as error:
            print(f"Error al procesar {ruta_pdf.name}: {error}")
            resultados.append({
                "archivo": ruta_pdf.name,
                "numero": None,
                "fecha": None,
                "emisor": None,
                "rut_emisor": None,
                "receptor": None,
                "rut_receptor": None,
                "monto_bruto": None,
                "retencion": None,
                "monto_liquido": None,
                "estado": f"Error: {error}",
            })

    columnas = [
        "archivo", "numero", "fecha", "emisor", "rut_emisor",
        "receptor", "rut_receptor", "monto_bruto", "retencion",
        "monto_liquido", "estado",
    ]

    df = pd.DataFrame(resultados, columns=columnas)
    archivo_excel.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(archivo_excel, index=False, engine="openpyxl")

    print(f"\nExcel generado: {archivo_excel}")
    print(f"Total de PDF procesados: {len(resultados)}")
    print(df[["archivo", "numero", "estado"]].to_string(index=False))



if __name__ == "__main__":
    carpeta_proyecto = Path(__file__).resolve().parent.parent
    carpeta_pdf = carpeta_proyecto / "data"
    archivo_excel = carpeta_proyecto / "output" / "boletas_procesadas.xlsx"

    print("Extractor de boletas - Etapa 5")
    print(f"Carpeta de entrada: {carpeta_pdf}")
    print(f"Archivo de salida: {archivo_excel}")

    procesar_carpeta(carpeta_pdf, archivo_excel)


