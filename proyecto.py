from datetime import datetime
import hashlib
import os
import json
import argparse


def calcular_hash(ruta):
    try:
        with open(ruta, "rb") as file:
            content = file.read()

        hash_archive = hashlib.sha256(content).hexdigest()

        return hash_archive

    except Exception as e:
        print(f"ERROR: No se pudo leer {ruta}")

        registrar_evento(
            "ERROR DE LECTURA",
            os.path.basename(ruta)
        )

        return None


def leer_hashes_actuales(carpeta):
    hashes = {}

    for nombre_archivo in os.listdir(carpeta):

        ruta = os.path.join(carpeta, nombre_archivo)

        if os.path.isfile(ruta):

            hash_archive = calcular_hash(ruta)

            if hash_archive is not None:
                hashes[nombre_archivo] = hash_archive

    return hashes


def enviar_diccionario(hashes):
    with open("hashes.json", "w") as archivo:
        json.dump(hashes, archivo, indent=4)


def leer_hashes_guardados():
    try:
        with open("hashes.json", "r") as archivo:
            hashes_guardados = json.load(archivo)

            return hashes_guardados

    except FileNotFoundError:
        print("El archivo con los hashes aún no existe")

        return "NO ARCHIVO"

    except json.JSONDecodeError:
        print("ERROR: hashes.json está corrupto o tiene un formato inválido")

        registrar_evento(
            "JSON CORRUPTO",
            "hashes.json"
        )

        return "CORRUPTO"


def detectar_modificacion(hashes_guardados, hashes_actuales):

    print("--------------- RESUMEN DE MONITOREO ----------------")

    cambio_detectado = False

    nuevos = 0
    modificados = 0
    eliminados = 0

    for archivo in hashes_actuales:

        if archivo not in hashes_guardados:

            cambio_detectado = True
            nuevos += 1

            print("Archivo Nuevo: " + archivo)

            registrar_evento(
                "ARCHIVO NUEVO",
                archivo
            )

        elif hashes_actuales[archivo] != hashes_guardados[archivo]:

            cambio_detectado = True
            modificados += 1

            print("Archivo Modificado: " + archivo)

            registrar_evento(
                "ARCHIVO MODIFICADO",
                archivo
            )

    for archivo in hashes_guardados:

        if archivo not in hashes_actuales:

            cambio_detectado = True
            eliminados += 1

            print("Archivo Eliminado: " + archivo)

            registrar_evento(
                "ARCHIVO ELIMINADO",
                archivo
            )

    if not cambio_detectado:
        print("No se detectaron cambios")

    print("\n--------------- ESTADÍSTICAS ----------------")

    print("Archivos nuevos:", nuevos)
    print("Archivos modificados:", modificados)
    print("Archivos eliminados:", eliminados)


def registrar_evento(tipo_evento, nombre_archivo):

    ahora = datetime.now()

    with open("monitor.log", "a") as archivo:

        archivo.write(
            "["
            + ahora.strftime("%Y-%m-%d %H:%M:%S")
            + "] "
            + tipo_evento
            + ": "
            + nombre_archivo
            + "\n"
        )


def obtener_argumentos():

    parser = argparse.ArgumentParser(
        description=(
            "File Integrity Monitor - "
            "Monitorea la integridad de archivos mediante SHA-256."
        )
    )

    parser.add_argument(
        "carpeta",
        help="Ruta de la carpeta que se desea monitorear"
    )

    return parser.parse_args()


def main():

    argumentos = obtener_argumentos()

    carpeta = argumentos.carpeta

    hashes_guardados = leer_hashes_guardados()

    if hashes_guardados == "CORRUPTO":

        print(
            "El archivo de hashes está corrupto, "
            "deteniendo programa"
        )

        return

    hashes_actuales = leer_hashes_actuales(carpeta)

    if hashes_guardados == "NO ARCHIVO":

        print(
            "--------------- FILE INTEGRITY MONITOR ---------------\n"
            "Primer registro de hashes guardado con éxito"
        )

    else:

        print("Revisión realizada")

        detectar_modificacion(
            hashes_guardados,
            hashes_actuales
        )

    enviar_diccionario(hashes_actuales)


main()