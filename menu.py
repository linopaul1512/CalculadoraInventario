#!/usr/bin/python3
import pathlib
from tkinter import DISABLED
import tkinter
import pygubu
import pygubuinterservices_Main
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "menu.ui"


class MenuApp:
    def __init__(self,type, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)
      
        self.type=type
        
        self.buttonservices = builder.get_object('buttonservices')
        self.buttoncalculations = builder.get_object('buttoncalculations')
        self.buttonreport = builder.get_object('buttonreport')

        self.buttonserviceorden = builder.get_object('buttonserviceorden')
        self.buttonmaterialorden = builder.get_object('buttonmaterialorden')
        self.buttonlabourorden = builder.get_object('buttonlabourorden')

        if (self.type!='Administrator'):
            self.buttonservices['state']='disabled'
            self.buttoncalculations['state']='disabled'
            self.buttonreport['state']='disabled'

            self.buttonserviceorden['state']='disabled'
            self.buttonmaterialorden['state']='disabled'
            self.buttonlabourorden['state']='disabled'

    def run(self):
     self.mainwindow.mainloop()

    
    def show_order(self):
        orden = pygubuorden_Main.OrdensApp()
        orden.run()

        
    def show_customer(self):
        client = pygubuclient_Main.ClientApp()
        client.run()

    def show_material(self):
        material = pygubumaterial_Main.MaterialApp()
        material.run()

    def show_services(self):
        service = pygubuservices_Main.ServicesApp()
        service.run()

    def show_labour(self):
        labour = pygubulabour_Main.LabourApp()
        labour.run()

    def show_calculations(self):
        calculations = pygubucalculations_Main.CalculationsApp()
        calculations.run()

    def show_report(self):
        pass

    def show_serviceorden(self):
        serviceorden = pygubuinterservices_Main.InterserviceApp()
        serviceorden.run()

    """def show_labourorden(self):
        labourorden = pygubuinterlabour_Main.LabourinterApp()
        labourorden.run()"""

    def show_materialorden(self):
        materialorden = pygubuintermaterial_Main.MaterialinterApp()
        materialorden.run()

if __name__ == "__main__":
    app = MenuApp()
    app.run()
