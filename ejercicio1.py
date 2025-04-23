import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


class Aplication:
    def __init__(self) -> None:
        self.ventana = tk.Tk()
        self.ventana.title("Clasificación ABC")
        self.ventana.geometry("600x600")

        # Títulos
        tk.Label(self.ventana, text="Clasificación ABC de productos", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.ventana, text="Ingrese el vector de demanda (uso anual), separado por comas:").pack()
        self.consumo_entry = tk.Entry(self.ventana, width=60)
        self.consumo_entry.pack()

        tk.Label(self.ventana, text="Ingrese el vector de costo unitario, separado por comas:").pack()
        self.costo_entry = tk.Entry(self.ventana, width=60)
        self.costo_entry.pack()

        # Botón de procesamiento
        tk.Button(self.ventana, text="Calcular clasificación ABC", command=self.calcular_abc).pack(pady=15)

        # Tabla
        self.tree = ttk.Treeview(self.ventana, columns=("Producto", "Clasificación"), show='headings')
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Clasificación", text="Clasificación ABC")
        self.tree.pack(pady=20, fill="both", expand=True)

        self.ventana.mainloop()

    def calcular_abc(self):
        try:
            demanda = list(map(float, self.consumo_entry.get().split(',')))
            costos = list(map(float, self.costo_entry.get().split(',')))

            if len(demanda) != len(costos):
                messagebox.showerror("Error", "Los vectores deben tener la misma longitud.")
                return

            productos = [chr(97 + i) for i in range(len(demanda))]  # a, b, c, ...
            valores_anuales = [d * c for d, c in zip(demanda, costos)]
            total_inventario = sum(valores_anuales)

            datos = list(zip(productos, demanda, costos, valores_anuales))
            datos.sort(key=lambda x: x[3], reverse=True)

            # Clasificación ABC
            acumulado = 0
            clasificacion = {}

            for prod, uso, costo, valor in datos:
                acumulado += valor
                porcentaje = acumulado / total_inventario
                if porcentaje <= 0.8:
                    clasificacion[prod] = 'A'
                elif porcentaje <= 0.95:
                    clasificacion[prod] = 'B'
                else:
                    clasificacion[prod] = 'C'

            # Limpiar tabla anterior
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Cargar nueva data
            for prod in productos:
                self.tree.insert('', 'end', values=(prod.upper(), clasificacion[prod]))

            # Mostrar gráfico
            self.mostrar_grafico(productos, valores_anuales)

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar los datos: {e}")

    def mostrar_grafico(self, productos, valores):
        ordenados = sorted(zip(productos, valores), key=lambda x: x[1], reverse=True)
        total = sum(valores)
        acumulado = 0
        porcentaje = []

        for _, valor in ordenados:
            acumulado += valor
            porcentaje.append(acumulado / total * 100)

        etiquetas = [p.upper() for p, _ in ordenados]

        plt.figure(figsize=(10, 5))
        plt.plot(etiquetas, porcentaje, marker='o')
        plt.title("Porcentaje acumulado de valor anual por producto")
        plt.xlabel("Producto")
        plt.ylabel("Porcentaje acumulado (%)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def main():
    Aplication()


if __name__ == "__main__":
    main()
