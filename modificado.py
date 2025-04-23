import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


class Aplication:
    def __init__(self) -> None:
        self.ventana = tk.Tk()
        self.ventana.title("Clasificación ABC Extendida")
        self.ventana.geometry("1000x600")

        # Entradas de usuario
        tk.Label(self.ventana, text="Demanda anual (uso), separado por comas:").pack()
        self.consumo_entry = tk.Entry(self.ventana, width=100)
        self.consumo_entry.pack()

        tk.Label(self.ventana, text="Costo unitario, separado por comas:").pack()
        self.costo_entry = tk.Entry(self.ventana, width=100)
        self.costo_entry.pack()

        tk.Label(self.ventana, text="Nombres de los productos, separados por comas:").pack()
        self.lista_productos = tk.Entry(self.ventana, width=100)
        self.lista_productos.pack()

        tk.Button(self.ventana, text="Calcular clasificación ABC", command=self.calcular_abc).pack(pady=10)

          #nombres: harina, jugo, papel, cebolla, jamon, queso, pan, tequeños, frescolita, malta, 7up, jabon, papas, toddy, doritos, nucita, chocolate,  cambur, cereal
        # vector demanda:  80,514,19,2442,650,128,2500,4,25,2232,2,1,6,12,101,715,1,35,1
        #vector costo: 422,54.07,0.65,16.11,4.61,0.63,1.2,22.05,5.01,2.48,4.78,38.03,9.01,25.89,59.5,20.78,2.93,1,28.88

        # Tabla extendida
        columnas = ("Producto", "A", "B", "C", "D", "E", "Clasificación")
        self.tree = ttk.Treeview(self.ventana, columns=columnas, show='headings')
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)

        self.ventana.mainloop()

    def calcular_abc(self):
        try:
            demanda = list(map(float, self.consumo_entry.get().split(',')))
            costos = list(map(float, self.costo_entry.get().split(',')))
            nombres = list(map(str, self.lista_productos.get().split(',')))

            if not (len(demanda) == len(costos) == len(nombres)):
                messagebox.showerror("Error", "Los tres vectores deben tener la misma longitud.")
                return

            # Cálculo de valores
            valores_uso = [d * c for d, c in zip(demanda, costos)]
            total_valor_uso = sum(valores_uso)

            # % uso anual del dinero (D)
            porcentajes = [(v * 100) / total_valor_uso for v in valores_uso]

            # Crear lista de datos con acumulado
            datos = list(zip(nombres, demanda, costos, valores_uso, porcentajes))
            datos.sort(key=lambda x: x[3], reverse=True)  # ordenar por valor de uso (C)

            # % acumulado y clasificación
            acumulado = 0
            datos_finales = []

            for nombre, uso, costo, valor, porcentaje in datos:
                acumulado += porcentaje
                if acumulado <= 80:
                    clase = 'A'
                elif acumulado <= 95:
                    clase = 'B'
                else:
                    clase = 'C'

                datos_finales.append((nombre, uso, costo, valor, round(porcentaje, 2), round(acumulado, 2), clase))

            # Mostrar en tabla
            for row in self.tree.get_children():
                self.tree.delete(row)
            for fila in datos_finales:
                self.tree.insert("", "end", values=fila)

            # Mostrar gráfico
            self.mostrar_grafico(datos_finales)

        except Exception as e:
            messagebox.showerror("Error", f"Error en el procesamiento: {e}")

    def mostrar_grafico(self, datos):
        productos = [d[0] for d in datos]
        acumulados = [d[5] for d in datos]

        plt.figure(figsize=(10, 5))
        plt.plot(productos, acumulados, marker='o')
        plt.title("Porcentaje acumulado del valor de uso")
        plt.xlabel("Producto")
        plt.ylabel("% Acumulado del dinero")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def main():
    Aplication()


if __name__ == "__main__":
    main()
