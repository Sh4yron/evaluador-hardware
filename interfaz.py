# Interfaz gráfica con menú lateral - Sistema de Evaluación de Hardware
import customtkinter as ctk
from tkinter import messagebox
from modelos import Equipo
from base_datos import (
    guardar_equipo,
    obtener_historial,
    buscar_equipo_por_id,
    eliminar_equipo_por_id,
)
from reportes import exportar_a_csv


def limpiar_contenido(contenido):
    """Borra lo que hay en el panel derecho para mostrar otra pantalla."""
    for elemento in contenido.winfo_children():
        elemento.destroy()


def crear_sidebar(ventana, contenido):
    """Crea el menú lateral izquierdo con los botones principales."""
    sidebar = ctk.CTkFrame(ventana, width=190, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    ctk.CTkLabel(
        sidebar, text="MENÚ PRINCIPAL", font=("Arial", 16, "bold")
    ).pack(pady=(25, 20))

    ctk.CTkButton(
        sidebar, text="Inicio", command=lambda: mostrar_inicio(contenido)
    ).pack(fill="x", padx=15, pady=6)

    ctk.CTkButton(
        sidebar, text="Evaluar Equipo", command=lambda: mostrar_evaluar(contenido)
    ).pack(fill="x", padx=15, pady=6)

    ctk.CTkButton(
        sidebar, text="Historial", command=lambda: mostrar_historial(contenido)
    ).pack(fill="x", padx=15, pady=6)

    ctk.CTkButton(
        sidebar, text="Exportar CSV", command=lambda: mostrar_exportar(contenido)
    ).pack(fill="x", padx=15, pady=6)


def mostrar_inicio(contenido):
    """Muestra la pantalla principal con el total de equipos guardados."""
    limpiar_contenido(contenido)
    total = len(obtener_historial())

    ctk.CTkLabel(
        contenido, text="Sistema de Evaluación de Hardware", font=("Arial", 22, "bold")
    ).pack(pady=(35, 10))

    ctk.CTkLabel(
        contenido,
        text="Evalúa componentes de PC, calcula su precio estimado\ny guarda los datos en SQLite.",
        font=("Arial", 14),
    ).pack(pady=10)

    tarjeta = ctk.CTkFrame(contenido, corner_radius=12)
    tarjeta.pack(pady=25, padx=40, fill="x")

    ctk.CTkLabel(
        tarjeta,
        text=f"Equipos registrados en la base de datos: {total}",
        font=("Arial", 16, "bold"),
    ).pack(pady=25)


def procesar_evaluacion(entrada_so, entrada_proc, entrada_ram, entrada_ssd, label_resultado):
    """Valida los campos, crea el objeto Equipo y lo guarda en SQLite."""
    so = entrada_so.get().strip()
    proc = entrada_proc.get().strip()
    if not so or not proc:
        messagebox.showwarning("Campos vacíos", "Debe llenar el sistema operativo y el procesador.")
        return

    try:
        ram = int(entrada_ram.get().strip())
        ssd = int(entrada_ssd.get().strip())
    except ValueError:
        messagebox.showerror("Dato inválido", "La RAM y el disco SSD deben ser números enteros.")
        return

    if ram <= 0 or ssd <= 0:
        messagebox.showwarning("Valor inválido", "La RAM y el disco SSD deben ser mayores a 0.")
        return

    equipo = Equipo(so, proc, ram, ssd)
    guardar_equipo(equipo)

    if equipo.veredicto == "Equipo recomendado":
        color = "green"
    elif equipo.veredicto == "Equipo no recomendado":
        color = "red"
    else:
        color = "orange"

    label_resultado.configure(
        text=f"{equipo.veredicto}  |  Precio Est.: RD$ {equipo.precio_estimado:,.2f}",
        text_color=color,
    )
    entrada_so.delete(0, "end")
    entrada_proc.delete(0, "end")
    entrada_ram.delete(0, "end")
    entrada_ssd.delete(0, "end")


def mostrar_evaluar(contenido):
    """Muestra el formulario para registrar y evaluar un equipo."""
    limpiar_contenido(contenido)
    ctk.CTkLabel(
        contenido, text="Evaluar Nuevo Equipo", font=("Arial", 20, "bold")
    ).pack(pady=(20, 15))

    ctk.CTkLabel(contenido, text="Sistema Operativo (Ej: Windows 11):", anchor="w").pack(fill="x", padx=50)
    entrada_so = ctk.CTkEntry(contenido, height=32)
    entrada_so.pack(fill="x", padx=50, pady=(2, 10))

    ctk.CTkLabel(contenido, text="Procesador (Ej: Core i5, Ryzen 5):", anchor="w").pack(fill="x", padx=50)
    entrada_proc = ctk.CTkEntry(contenido, height=32)
    entrada_proc.pack(fill="x", padx=50, pady=(2, 10))

    ctk.CTkLabel(contenido, text="Memoria RAM (GB):", anchor="w").pack(fill="x", padx=50)
    entrada_ram = ctk.CTkEntry(contenido, height=32)
    entrada_ram.pack(fill="x", padx=50, pady=(2, 10))

    ctk.CTkLabel(contenido, text="Almacenamiento SSD (GB):", anchor="w").pack(fill="x", padx=50)
    entrada_ssd = ctk.CTkEntry(contenido, height=32)
    entrada_ssd.pack(fill="x", padx=50, pady=(2, 10))

    label_resultado = ctk.CTkLabel(contenido, text="", font=("Arial", 14, "bold"))
    ctk.CTkButton(
        contenido,
        text="Evaluar y Guardar",
        height=38,
        command=lambda: procesar_evaluacion(
            entrada_so, entrada_proc, entrada_ram, entrada_ssd, label_resultado
        ),
    ).pack(pady=10)
    label_resultado.pack(pady=5)


def mostrar_lista(contenedor, registros):
    """Muestra cada equipo guardado como una tarjeta dentro de la lista."""
    limpiar_contenido(contenedor)
    if not registros:
        ctk.CTkLabel(
            contenedor, text="No hay equipos registrados todavía.", font=("Arial", 14)
        ).pack(pady=30)
        return

    for eq in registros:
        tarjeta = ctk.CTkFrame(contenedor, corner_radius=8)
        tarjeta.pack(fill="x", padx=8, pady=5)
        texto = (
            f"ID #{eq[0]}  |  {eq[1]} - {eq[2]}  |  RAM: {eq[3]} GB  |  SSD: {eq[4]} GB\n"
            f"Precio Est.: RD$ {eq[6]:,.2f}   •   {eq[5]}"
        )
        ctk.CTkLabel(tarjeta, text=texto, justify="left", anchor="w").pack(
            fill="x", padx=12, pady=8
        )


def buscar_por_id(entrada_id, contenedor):
    """Busca un equipo por su número de ID y lo muestra."""
    try:
        id_buscado = int(entrada_id.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número de ID válido.")
        return

    registro = buscar_equipo_por_id(id_buscado)
    if not registro:
        messagebox.showinfo("No encontrado", f"No existe ningún equipo con ID #{id_buscado}.")
        return
    mostrar_lista(contenedor, [registro])


def eliminar_por_id(entrada_id, contenedor):
    """Elimina un equipo por su ID y actualiza la lista."""
    try:
        id_borrar = int(entrada_id.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número de ID válido.")
        return

    if eliminar_equipo_por_id(id_borrar):
        messagebox.showinfo("Eliminado", f"Equipo ID #{id_borrar} eliminado.")
        entrada_id.delete(0, "end")
        mostrar_lista(contenedor, obtener_historial())
    else:
        messagebox.showwarning("No encontrado", f"No se encontró el ID #{id_borrar}.")


def mostrar_historial(contenido):
    """Muestra el historial completo y los botones para buscar o eliminar."""
    limpiar_contenido(contenido)
    ctk.CTkLabel(
        contenido, text="Historial de Equipos", font=("Arial", 20, "bold")
    ).pack(pady=(15, 10))

    barra = ctk.CTkFrame(contenido, fg_color="transparent")
    barra.pack(fill="x", padx=25, pady=5)

    entrada_id = ctk.CTkEntry(barra, placeholder_text="ID...", width=80)
    entrada_id.pack(side="left", padx=5)

    lista = ctk.CTkScrollableFrame(contenido, height=330)

    ctk.CTkButton(
        barra, text="Buscar", width=80, command=lambda: buscar_por_id(entrada_id, lista)
    ).pack(side="left", padx=4)
    ctk.CTkButton(
        barra, text="Eliminar", width=80, fg_color="red", hover_color="darkred",
        command=lambda: eliminar_por_id(entrada_id, lista)
    ).pack(side="left", padx=4)
    ctk.CTkButton(
        barra, text="Ver Todos", width=85,
        command=lambda: mostrar_lista(lista, obtener_historial())
    ).pack(side="left", padx=4)

    lista.pack(fill="both", expand=True, padx=25, pady=10)
    mostrar_lista(lista, obtener_historial())


def ejecutar_exportacion(label_estado):
    """Llama a la función que exporta los registros a un archivo CSV."""
    registros = obtener_historial()
    if exportar_a_csv(registros):
        label_estado.configure(
            text="¡Archivo 'reporte_equipos.csv' creado correctamente!",
            text_color="green",
        )
    else:
        messagebox.showwarning("Sin datos", "No hay equipos guardados para exportar.")


def mostrar_exportar(contenido):
    """Muestra la pantalla para exportar el historial a Excel/CSV."""
    limpiar_contenido(contenido)
    ctk.CTkLabel(
        contenido, text="Exportar Reporte a CSV", font=("Arial", 20, "bold")
    ).pack(pady=(40, 15))

    ctk.CTkLabel(
        contenido,
        text="Genera un archivo CSV con todos los equipos guardados\nen la base de datos.",
        font=("Arial", 14),
    ).pack(pady=10)

    label_estado = ctk.CTkLabel(contenido, text="", font=("Arial", 13, "bold"))
    ctk.CTkButton(
        contenido,
        text="Generar reporte_equipos.csv",
        height=40,
        command=lambda: ejecutar_exportacion(label_estado),
    ).pack(pady=20)
    label_estado.pack(pady=10)


def iniciar_aplicacion():
    """Configura el modo oscuro, crea la ventana principal y la ejecuta."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Sistema de Evaluación de Hardware")
    ventana.geometry("820x520")

    contenido = ctk.CTkFrame(ventana, corner_radius=0)
    contenido.pack(side="right", fill="both", expand=True)

    crear_sidebar(ventana, contenido)
    mostrar_inicio(contenido)
    ventana.mainloop()