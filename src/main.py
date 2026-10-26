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
    ruta =  "data/PRUEBA_ficticia_boleta_1001.pdf"  
    texto = leer_texto(ruta)
    print(texto)
