"""Módulo encargado de la conexión y operaciones con SQLite."""
import sqlite3


def conectar_db():
    """Crea y devuelve la conexión a la base de datos SQLite."""
    return sqlite3.connect("hardware_evaluacion.db")


def inicializar_base_datos():
    """Crea la tabla equipos si todavía no existe."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sistema_operativo TEXT NOT NULL,
            procesador TEXT NOT NULL,
            memoria_ram INTEGER NOT NULL,
            almacenamiento_ssd INTEGER NOT NULL,
            veredicto TEXT NOT NULL,
            precio_estimado REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()


def guardar_equipo(equipo):
    """Guarda un objeto Equipo en la base de datos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO equipos (sistema_operativo, procesador, memoria_ram, almacenamiento_ssd, veredicto, precio_estimado)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            equipo.sistema_operativo,
            equipo.procesador,
            equipo.memoria_ram,
            equipo.almacenamiento_ssd,
            equipo.veredicto,
            equipo.precio_estimado,
        ),
    )
    conexion.commit()
    conexion.close()


def obtener_historial():
    """Devuelve todos los registros guardados en la tabla equipos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos")
    registros = cursor.fetchall()
    conexion.close()
    return registros


def buscar_equipo_por_id(id_equipo):
    """Busca un equipo por su ID y devuelve su registro o None si no existe."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos WHERE id = ?", (id_equipo,))
    registro = cursor.fetchone()
    conexion.close()
    return registro


def eliminar_equipo_por_id(id_equipo):
    """Elimina un equipo por su ID. Devuelve True si se borró o False si no existía."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM equipos WHERE id = ?", (id_equipo,))
    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0