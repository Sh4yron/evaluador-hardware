"""Módulo que define la clase Equipo y las reglas de evaluación."""


class Equipo:
    """Representa un equipo de cómputo a evaluar."""

    def __init__(self, sistema_operativo, procesador, memoria_ram, almacenamiento_ssd):
        self.sistema_operativo = sistema_operativo.strip().title()
        self.procesador = procesador.strip().title()
        self.memoria_ram = int(memoria_ram)
        self.almacenamiento_ssd = int(almacenamiento_ssd)
        self.veredicto = self.calcular_veredicto()
        self.precio_estimado = self.calcular_precio()

    def calcular_veredicto(self):
        """Determina si el equipo es recomendado según su RAM y SSD."""
        if self.memoria_ram >= 16 and self.almacenamiento_ssd >= 512:
            return "Equipo recomendado"
        elif self.memoria_ram < 16 and self.almacenamiento_ssd < 512:
            return "Equipo no recomendado"
        else:
            return "Equipo funcional con limitaciones"

    def calcular_precio(self):
        """Calcula el precio estimado en pesos dominicanos (RD$)."""
        return 8000 + (self.memoria_ram * 800) + (self.almacenamiento_ssd * 5)