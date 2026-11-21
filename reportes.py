"""Módulo encargado de exportar los registros a un archivo CSV."""
import csv


def exportar_a_csv(registros, nombre_archivo="reporte_equipos.csv"):
    """Exporta la lista de equipos a un archivo CSV. Devuelve True si tuvo éxito."""
    if not registros:
        return False

    encabezados = [
        "ID",
        "Sistema Operativo",
        "Procesador",
        "RAM (GB)",
        "SSD (GB)",
        "Veredicto",
        "Precio Estimado (RD$)",
    ]

    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        escritor.writerows(registros)

    return True