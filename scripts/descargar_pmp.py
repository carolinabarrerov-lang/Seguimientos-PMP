"""Descarga los originales publicados por ANI; solo requiere Python 3."""
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[1]


def descargar():
    fuentes = json.loads((ROOT / "datos/fuentes.json").read_text(encoding="utf-8"))
    destino = ROOT / "datos/originales"
    destino.mkdir(parents=True, exist_ok=True)
    errores = 0
    for fuente in fuentes:
        temporal = destino / (fuente["corte"] + ".part")
        try:
            request = Request(fuente["url"], headers={"User-Agent": "Seguimientos-PMP/1.0"})
            with urlopen(request, timeout=120) as response:
                inicio = response.read(8192)
                if inicio.startswith(b"%PDF-"):
                    extension = ".pdf"
                elif inicio.startswith(b"PK\x03\x04"):
                    extension = ".xlsx"
                elif inicio.startswith(bytes.fromhex("D0CF11E0A1B11AE1")):
                    extension = ".xls"
                else:
                    raise ValueError("Respuesta no reconocida como PDF o Excel; no se guardará como base de datos")
                with temporal.open("wb") as salida:
                    salida.write(inicio)
                    while True:
                        bloque = response.read(1024 * 1024)
                        if not bloque:
                            break
                        salida.write(bloque)
            archivo = destino / ("pmp_" + fuente["corte"] + extension)
            temporal.replace(archivo)
            print(f"Descargado: {archivo.relative_to(ROOT)}")
        except (OSError, URLError, ValueError) as error:
            temporal.unlink(missing_ok=True)
            errores += 1
            print(f"No se pudo descargar {fuente['corte']}: {error}", file=sys.stderr)
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(descargar())
