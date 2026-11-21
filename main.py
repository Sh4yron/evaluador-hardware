"""Archivo principal que inicia el Sistema de Evaluación de Hardware."""
from base_datos import inicializar_base_datos
from interfaz import iniciar_aplicacion


def main():
    """Inicializa la base de datos y abre la ventana principal."""
    inicializar_base_datos()
    iniciar_aplicacion()


if __name__ == "__main__":
    main()