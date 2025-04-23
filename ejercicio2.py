import tkinter as tk
from tkinter import ttk, messagebox
import math

class MenuModelosInventario:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Modelo de Inventario - Ejercicio 2")
        self.ventana.geometry("400x300")

        tk.Label(self.ventana, text="¿Qué desea calcular?", font=("Arial", 14, "bold")).pack(pady=10)

        # Selector de unidad de tiempo
        tk.Label(self.ventana, text="Seleccione la unidad de tiempo:").pack()
        self.unidad_tiempo = ttk.Combobox(self.ventana, values=["Días", "Semanas", "Meses", "Años"], state="readonly")
        self.unidad_tiempo.current(0)
        self.unidad_tiempo.pack(pady=5)

        # Selector de modelo
        tk.Label(self.ventana, text="Seleccione el modelo de inventario:").pack()
        self.modelo_estudio = ttk.Combobox(self.ventana, values=["Lote económico", "Descuento", "Probabilístico"], state="readonly")
        self.modelo_estudio.current(0)
        self.modelo_estudio.pack(pady=5)

        # Botón para continuar
        tk.Button(self.ventana, text="Calcular", command=self.ejecutar_modelo).pack(pady=20)

        self.ventana.mainloop()

    def ejecutar_modelo(self):
        tiempo = self.unidad_tiempo.get()
        modelo = self.modelo_estudio.get()

        try:
            if modelo == "Lote económico":
                self.ventana.destroy()
                self.lote_economico_interface()
            elif modelo == "Descuento":
                self.ventana.destroy()
                self.descuento_interface()
            elif modelo == "Probabilístico":
                self.ventana.destroy()
                self.probabilistico_interface()
            else:
                raise ValueError("Modelo no reconocido.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def descuento_interface(self):
        def calcular():
            try:
                K = float(entry_k.get())
                D = float(entry_d.get())
                h_percent = float(entry_h.get()) / 100
                n = int(entry_n.get())

                tabla = []
                for i in range(n):
                    min_q = float(rangos[i][0].get())
                    max_q = rangos[i][1].get()
                    max_q = float('inf') if max_q.lower() == 'inf' else float(max_q)
                    precio = float(rangos[i][2].get())
                    tabla.append((min_q, max_q, precio))

                opciones = []
                for (b_min, b_max, precio_unitario) in tabla:
                    h = h_percent * precio_unitario
                    EOQ = math.sqrt((2 * K * D) / h)
                    q = EOQ if b_min <= EOQ < b_max else (b_min if EOQ < b_min else EOQ)
                    if q == 0:
                        continue
                    CT = (K * D / q) + (h * q / 2) + (precio_unitario * D)
                    opciones.append((q, precio_unitario, CT))

                mejor_opcion = min(opciones, key=lambda x: x[2])

                messagebox.showinfo("Resultado",
                    f"Cantidad óptima de pedido: {mejor_opcion[0]:.2f}\n"
                    f"Frecuencia óptima: {D / mejor_opcion[0]:.2f}\n"
                    f"Precio por unidad: ${mejor_opcion[1]:.2f}\n"
                    f"Costo total anual: ${mejor_opcion[2]:.2f}")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ventana = tk.Tk()
        ventana.title("Modelo de Descuento")
        ventana.geometry("500x600")

        tk.Label(ventana, text="Costo de ordenar (K):").pack()
        entry_k = tk.Entry(ventana)
        entry_k.pack()

        tk.Label(ventana, text="Demanda anual (D):").pack()
        entry_d = tk.Entry(ventana)
        entry_d.pack()

        tk.Label(ventana, text="Costo de almacenaje (%):").pack()
        entry_h = tk.Entry(ventana)
        entry_h.pack()

        tk.Label(ventana, text="Número de rangos de descuento:").pack()
        entry_n = tk.Entry(ventana)
        entry_n.pack()

        rangos = []

        def crear_campos():
            nonlocal rangos
            for widget in frame_rangos.winfo_children():
                widget.destroy()
            rangos.clear()
            for i in range(int(entry_n.get())):
                tk.Label(frame_rangos, text=f"Rango #{i+1}").grid(row=i, column=0)
                min_q = tk.Entry(frame_rangos, width=10)
                min_q.grid(row=i, column=1)
                max_q = tk.Entry(frame_rangos, width=10)
                max_q.grid(row=i, column=2)
                precio = tk.Entry(frame_rangos, width=10)
                precio.grid(row=i, column=3)
                rangos.append((min_q, max_q, precio))

        tk.Button(ventana, text="Crear campos de descuento", command=crear_campos).pack(pady=5)
        frame_rangos = tk.Frame(ventana)
        frame_rangos.pack(pady=10)

        tk.Button(ventana, text="Calcular", command=calcular).pack(pady=20)
        ventana.mainloop()

    def lote_economico_interface(self):
        messagebox.showinfo("Modelo", "Interfaz para lote económico (a implementar)")

    def probabilistico_interface(self):
        messagebox.showinfo("Modelo", "Interfaz para modelo probabilístico (a implementar)")


def main():
    MenuModelosInventario()


if __name__ == "__main__":
    main()
