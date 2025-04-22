import tkinter as tk
from tkinter import ttk



class Aplication:
    def __init__(self)-> None:
        self.ventana = tk.Tk()
        self.ventana.title("Ejercicio 4")
        self.ventana.geometry("500x500+500+150")
    #    self.ventana.config(bg="#A1F508", cursor="gumby")
        
        
     

       #Titulo label
        self.label = tk.Label(self.ventana, text="Clasificacion ABC")
        self.label.place(x=10, y=80)
        
        
        #Titulo 
        self.label = tk.Label(self.ventana, text="Ingrese el vector de demanda separado por comas (,)")
        self.label.place(x=10, y=100)
        
        #Entry
        self.entrada_text1 = tk.Entry(
            self.ventana,
            width = 30,
            font= ("Arial,18")
        )
        self.entrada_text1.place(x=10, y=120)
        
        #Titulo 
        self.label = tk.Label(self.ventana, text="Ingrese el vector de costo unitario separado por comas (,)")
        self.label.place(x=10, y=140)
        
        #Entry
        self.entrada_text2 = tk.Entry(
            self.ventana,
            width = 30,
            font= ("Arial,18")
        )
        self.entrada_text2.place(x=10, y=160)
        
        
        self.tree = ttk.Treeview(
        self.balance_wind, height=10, columns=[f"#{n}" for n in range(1, 10)])
        
        


        self.ventana.mainloop()


def main():
    Aplication()

if __name__ == "__main__":
    main()



           