import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt


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
            elif modelo == "Cola M/M/1":
                self.ventana.destroy()
                self.cola()
            else:
                raise ValueError("Modelo no reconocido.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    
        """Medida	Resultado
            Clientes en el sistema (L)	3 clientes
            Clientes en la cola (Lq)	2.25 clientes
            Tiempo promedio en sistema (W)	1 hora
            Tiempo promedio en cola (Wq)	0.75 horas
            Probabilidad de 3 clientes (P(3))	0.1055 (aprox 10.5%)
            Probabilidad de esperar más de 1 hora	0.3679 (aprox 36.8%)
            Probabilidad de más de 5 clientes	0.178 (aprox 17.8%)
        """
    def descuento_interface(self):
        def calcular():
            try:
                precio_base = float(entry_precio_base.get())
                q = float(entry_q.get())
                D = float(entry_d.get())
                cantidad_rangos_descuentos = int(entry_n.get())

                tabla = []
                for i in range(cantidad_rangos_descuentos):
                    min_q = float(rangos[i][0].get())
                    max_q = rangos[i][1].get()
                    #para infitino
                    max_q = float('inf') if max_q == "inf" else float(max_q)
                    descuento = float(rangos[i][2].get())
                    precio_unitario = precio_base * (1 - descuento / 100)
                    h_mes = float(rangos[i][3].get())
                    K_prep = float(rangos[i][4].get())
                    tabla.append((min_q, max_q, precio_unitario, h_mes, K_prep))

                costo_total = None
                for (b_min, b_max, precio_unitario, h, K) in tabla:
                    if b_min <= q <= b_max:
                        CT = (precio_unitario * D) + (K * D / q) + (h * q / 2)
                        costo_total = CT
                        break


                if costo_total is not None:
                    mensaje = f"Costo total mensual: ${costo_total:.2f}"
                    messagebox.showinfo("Resultado", mensaje)
                else:
                    messagebox.showwarning("Advertencia", "La cantidad (q) no está en ningún rango.")

                

            except Exception as e:
                messagebox.showerror("Error", str(e))

        def crear_campos():
            nonlocal rangos
            for widget in frame_rangos.winfo_children(): #winfo_children:obtener lista de widgets secundarios
                widget.destroy()
            rangos.clear()
            header = ["Min Q", "Max Q", "% Desc", "h (almac.)", "K (prep.)"]
            for i, h in enumerate(header):
                tk.Label(frame_rangos, text=h).grid(row=0, column=i)

            for i in range(int(entry_n.get())):
                fila = []
                for j in range(5): #5 columnas  #width:ancho en p
                    e = tk.Entry(frame_rangos, width=10)
                    e.grid(row=i+1, column=j)
                    fila.append(e)
                rangos.append(fila)

        # UI principal
        ventana = tk.Tk()
        ventana.title("Modelo de Descuento por Rango")
        ventana.geometry("650x750")

        tk.Label(ventana, text="Precio base del producto c (sin descuento):").pack()
        entry_precio_base = tk.Entry(ventana)
        entry_precio_base.pack()

        tk.Label(ventana, text="Demanda mensual (D):").pack()
        entry_d = tk.Entry(ventana)
        entry_d.pack()

        tk.Label(ventana, text="Cantidad del pedido (q):").pack()
        entry_q = tk.Entry(ventana)
        entry_q.pack()

        tk.Label(ventana, text="Número de rangos de descuento:").pack()
        entry_n = tk.Entry(ventana)
        entry_n.pack()

        tk.Button(ventana, text="Crear campos", command=crear_campos).pack(pady=5)

        frame_rangos = tk.Frame(ventana)
        frame_rangos.pack(pady=10)

        rangos = []

        tk.Button(ventana, text="Calcular", command=calcular).pack(pady=20)
        ventana.mainloop()

        

    def lote_economico_interface(self):
        def calcular():
            try:
                # Datos de entrada
                costo_pedido = float(entry_costo_pedido.get())  # S
                costo_almacenaje_mensual = float(entry_costo_almacenaje.get())  # h mensual
                tiempo_entrega_meses = float(entry_tiempo_entrega.get())  # L

                #S 
                #h
                #L

                #demanda_ano4 = [12, 50, 15, 110, 115, 90, 130, 75, 54, 160, 280, 41]
                #demanda_ano5 = [11, 55, 10, 120, 110, 100, 130, 78, 51, 180, 300, 43]

                demanda_ano4 = list(map(float, entry_demanda_ano4.get().split(',')))
                demanda_ano5 = list(map(float, entry_demanda_ano5.get().split(',')))


                if len(demanda_ano4) != 12 or len(demanda_ano5) != 12:
                    messagebox.showerror("Error", "Debes ingresar 12 valores para cada año, separados por comas.")
                    return

                #  Estimación según GERENTE
                # D * 0.10
                demanda_ano5_ajustada = [d * 0.10 for d in demanda_ano5]  # Año 5 +10%

                # Demanda anual gerente
                demanda_anual_gerente = sum(demanda_ano5_ajustada)

                #Sumatoria normal de la demanda
                suma_ano4  = sum(demanda_ano4)
                suma_ano5  = sum(demanda_ano5)
                
                # Demanda trimestral (cada 3 meses)
                pedidos_trimestrales = [
                    sum(demanda_ano5_ajustada[0:3]), #tri 1...
                    sum(demanda_ano5_ajustada[3:6]),
                    sum(demanda_ano5_ajustada[6:9]),
                    sum(demanda_ano5_ajustada[9:12])
                ]

                # Estimación según EMPLEADO
                demanda_promedio = [(a4 + a5) / 2 for a4, a5 in zip(demanda_ano4, demanda_ano5)]
                demanda_anual_empleado = sum(demanda_promedio)
                demanda_mensual_promedio = demanda_anual_empleado / 12

                costo_almacenaje_anual = costo_almacenaje_mensual * 12

                # Modelo EOQ (Empleado)
                Q = math.sqrt((2 * costo_pedido * demanda_anual_empleado) / costo_almacenaje_anual)

                #Tiempo entre pedidos
                T = math.sqrt((2 * costo_pedido) / (demanda_anual_empleado * costo_almacenaje_anual))  # en años
                T_meses = T * 12

                # Calcular punto de reorden (Empleado)
                if T_meses > tiempo_entrega_meses:
                    ROP = demanda_mensual_promedio * tiempo_entrega_meses
                else:
                    m = 0
                    while True:
                        if tiempo_entrega_meses - m * T_meses > 0 and tiempo_entrega_meses - (m + 1) * T_meses <= 0:
                            ROP = demanda_mensual_promedio * (tiempo_entrega_meses - m * T_meses)
                            break
                        m += 1



                # Resultudos por mensaje
                mensaje = "** Política del Gerente **\n"
                mensaje += f"Demanda anual segun vector 4 introducido: {suma_ano4:.2f} unidades\n"
                mensaje += f"Demanda anual segun vector 5 introducido: {suma_ano5:.2f} unidades\n"
                mensaje += f"Estimaciones de la demanda del año próximo: {demanda_anual_gerente:.2f} unidades\n"
                mensaje += "Pedidos trimestrales estimados:\n"
                mensaje += f"- Trimestre 1: {pedidos_trimestrales[0]:.2f} unidades\n"
                mensaje += f"- Trimestre 2: {pedidos_trimestrales[1]:.2f} unidades\n"
                mensaje += f"- Trimestre 3: {pedidos_trimestrales[2]:.2f} unidades\n"
                mensaje += f"- Trimestre 4: {pedidos_trimestrales[3]:.2f} unidades\n\n"

                mensaje += "===== Política del Empleado (Modelo EOQ) =====\n"
                mensaje += f"Demanda anual (promedio año 4 y 5): {demanda_anual_empleado:.2f} unidades\n"
                mensaje += f"Cantidad económica de pedido (Q): {Q:.2f} unidades\n"
                mensaje += f"Tiempo entre pedidos (T): {T_meses:.2f} meses\n"
                mensaje += f"Punto de reorden (ROP): {ROP:.2f} unidades"

                messagebox.showinfo("Resultado Comparativo", mensaje)

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # UI principal
        ventana = tk.Tk()
        ventana.title("Modelo de Lote Económico")
        ventana.geometry("700x800")

        tk.Label(ventana, text="Costo de colocar un pedido (S):").pack()
        entry_costo_pedido = tk.Entry(ventana)
        entry_costo_pedido.pack()

        tk.Label(ventana, text="Costo de almacenamiento mensual por unidad (h):").pack()
        entry_costo_almacenaje = tk.Entry(ventana)
        entry_costo_almacenaje.pack()

        tk.Label(ventana, text="Tiempo de entrega (en meses):").pack()
        entry_tiempo_entrega = tk.Entry(ventana)
        entry_tiempo_entrega.pack()

        tk.Label(ventana, text="Demanda del Año 4 (12 valores separados por comas):").pack()
        entry_demanda_ano4 = tk.Entry(ventana, width=70)
        entry_demanda_ano4.pack()

        tk.Label(ventana, text="Demanda del Año 5 (12 valores separados por comas):").pack()
        entry_demanda_ano5 = tk.Entry(ventana, width=70)
        entry_demanda_ano5.pack()

        tk.Button(ventana, text="Calcular", command=calcular).pack(pady=20)

        ventana.mainloop()
        
    def cola(self):
        def calcular():
                try:
                    # Obtener datos del usuario
                    tasa_llegada = float(entry_llegada.get())  # λ
                    tasa_servicio = float(entry_servicio.get())  # μ

                    if tasa_llegada >= tasa_servicio:
                        messagebox.showerror("Error", "La tasa de llegada debe ser menor que la tasa de servicio para un sistema estable.")
                        return

                    # Cálculos M/M/1
                    p = tasa_llegada / tasa_servicio  # Utilización
                    L = p / (1 - p)                   # Clientes en el sistema
                    Lq = p ** 2 / (1 - p)              # Clientes en la cola
                    W = 1 / (tasa_servicio - tasa_llegada)  # Tiempo en el sistema
                    Wq = p / (tasa_servicio - tasa_llegada) # Tiempo en la cola

                    # Probabilidades
                    P3 = (1 - p) * (p ** 3)  # Probabilidad de 3 clientes
                    P_mas_de_5 = p ** 6      # Probabilidad de más de 5 clientes
                    P_espera_mas_1hora = math.exp(-(tasa_servicio - tasa_llegada) * 1)  # Espera mayor a 1 hora

                    # Mostrar resultados
                    mensaje = "  Resultados M/M/1 \n"
                    mensaje += f"Clientes en el sistema (L): {L:.4f}\n"
                    mensaje += f"Clientes en la cola (Lq): {Lq:.4f}\n"
                    mensaje += f"Tiempo promedio en el sistema (W): {W:.4f} horas\n"
                    mensaje += f"Tiempo promedio en cola (Wq): {Wq:.4f} horas\n\n"

                    mensaje += " Probabilidades \n"
                    mensaje += f"Probabilidad de 3 clientes en el sistema: {P3:.4f}\n"
                    mensaje += f"Probabilidad de esperar más de 1 hora: {P_espera_mas_1hora:.4f}\n"
                    mensaje += f"Probabilidad de más de 5 clientes en el sistema: {P_mas_de_5:.4f}"

                    messagebox.showinfo("Resultados Modelo M/M/1", mensaje)

                except Exception as e:
                    messagebox.showerror("Error", str(e))

        # === UI principal ===
        ventana = tk.Tk()
        ventana.title("Modelo de Colas M/M/1 - Probabilístico")
        ventana.geometry("450x400")

        tk.Label(ventana, text="Tasa de llegada (clientes/hora) λ:").pack(pady=5)
        entry_llegada = tk.Entry(ventana)
        entry_llegada.pack()

        tk.Label(ventana, text="Tasa de servicio (clientes/hora) μ:").pack(pady=5)
        entry_servicio = tk.Entry(ventana)
        entry_servicio.pack()

        tk.Button(ventana, text="Calcular", command=calcular).pack(pady=20)

        ventana.mainloop()

        

            

def main():
    MenuModelosInventario()


if __name__ == "__main__":
    main()
