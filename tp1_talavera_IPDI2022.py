# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:17:24 2022

@author: Ema Talavera
"""

import tkinter as tk
#from tkinter import *
from tkinter import filedialog , messagebox, ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) 
import imageio.v2 as imageio
import numpy as np


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.methods = None
        self.file = None
        self.file_yiq = None
        self.file_rgb = None
        self.grid()
        self.create_widgets()
        self.value = 0.
        self.lum = '0'
        self.crom = '0'
        

    def create_widgets(self):
        self.methods = ("RGB to YIQ","YIQ to RGB")

        #self.quit = tk.Button(window, text="Salir", fg="red", command=window.destroy)
        #self.quit.place(x=450, y=500, width=100, height=30)
        #self.quit.grid(column=0, row=1)
        
        self.label_open= tk.Label(window, text="Seleccione un Archivo: ")
        self.label_open.grid(column=0, row=2, padx=(50,50), pady=(10,10))
        
        self.plot_button = tk.Button(window, command = self.open_file, height = 2, width = 15, text = "Abrir Imagen")
        self.plot_button.grid(column=1, row=2,  pady=(10,10))
        

    def change_space(self, event=None):
        space = self.combo.get()
        try:
            print("Metodo elegido ", space)
            if("RGB to YIQ"==space):
                print('Cambiar a YIQ')
                self.rgb_to_yiq()
            else:
                print('Cambiar a RGB')
                self.yiq_to_rgb(None, 'Imagen YIQ a RGB')
        except tk.TclError as err:
            messagebox.showerror('Error', err)
        else:
            window.title(space)
        
        
    def open_file(self):
        archivo = filedialog.askopenfilename(title="abrir", initialdir="C:/", filetypes = (("Archivos png", "*.png"), ("Archivos jpg", "*.jpg"), ("Archivos bmp", "*.bmp"), ("Todos lod archivos", "*.*")))
        if archivo:
            rgb = imageio.imread(archivo)/255.
            
            self.file = np.array(rgb)
            self.plot(rgb)
            
            self.label_combo = ttk.Label(window, text="Seleccione Metodo: ")
            self.label_combo.grid(column=0, row=4, pady=(10,10))
            
            self.combo = ttk.Combobox(window, values=self.methods)
            self.combo.grid(column=1, row=4, pady=(10,10))
            
            # boton cambiar espacio
            self.combo_button = tk.Button(window, text='Aceptar')
            self.combo_button['command'] = self.change_space
            self.combo_button.grid(column=2, row=4, pady=(10,10))
            
            # cambiar luminancia
            self.lum = tk.StringVar()
            self.label = ttk.Label(window, text="Luminancia")
            self.label.grid(column=0, row=5, padx=(10,10), pady=(10,10))
            self.lum = ttk.Entry(window, width=7, textvariable=self.lum)
            self.lum.grid(column=1, row=5, pady=(10,10))
            self.button_lum = tk.Button(window, text='Modificar Luminancia')
            self.button_lum['command'] = self.cambiar_luminancia
            self.button_lum.grid(column=3, row=5, padx=(10,10), pady=(10,10))
            
            # cambiar luminancia
            self.crom = tk.StringVar()
            self.label_crom = ttk.Label(window, text="Crominancia")
            self.label_crom.grid(column=0, row=6, padx=(10,10), pady=(10,10))
            self.crom = ttk.Entry(window, width=7, textvariable=self.lum)
            self.crom.grid(column=1, row=6, pady=(10,10))
            self.button_crom = tk.Button(window, text='Modificar Crominancia')
            self.button_crom['command'] = self.cambiar_crominancia
            self.button_crom.grid(column=3, row=6, padx=(10,10), pady=(10,10))
            
       
  
    def plot(self, file):
        
        fig = Figure(figsize = (3, 3), dpi = 100)
        plot = fig.add_subplot()
        plot.set_title('Imagen RGB')
        plot.imshow(file)
        
        self.canvas = FigureCanvasTkAgg(fig, master=window)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=3, columnspan=3, padx=(50,50), pady=(10,10))
        # toolbar = NavigationToolbar2Tk(canvas, window) 
        # toolbar.update() 
        # canvas.get_tk_widget().pack()
    
    def rgb_to_yiq(self):
        w = self.file.shape[0]
        h = self.file.shape[1]
        p=3
        yiq = np.zeros((w,h,p))
        #m_yiq.shape
        yiq[:,:,0] = 0.299 * self.file[:,:,0] + 0.587 * self.file[:,:,1] + 0.114 * self.file[:,:,2]
        yiq[:,:,1] = 0.595716 * self.file[:,:,0] + -0.274453 * self.file[:,:,1] + -0.321263 * self.file[:,:,2]
        yiq[:,:,2] = 0.211456 * self.file[:,:,0] + -0.522591 * self.file[:,:,1] + -0.321263 * self.file[:,:,2]
        
        yiq = np.clip(yiq,0.,1.)
        self.file_yiq = yiq
        
        """ Grafico de la imagen en el espacio YIQ """
        
        fig = Figure(figsize = (3, 3), dpi = 100)
        plot = fig.add_subplot()
        plot.set_title('Imagen YIQ')
        plot.imshow(yiq)
        
        self.canvas = FigureCanvasTkAgg(fig, master=window)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=4, row=0, columnspan=3, rowspan=4, padx=(10,10), pady=(10,10))
    
    def yiq_to_rgb(self, m_rgb, titulo: str):
        if(isinstance(m_rgb, type(None))):
            yiq = self.file_yiq
        else:
            yiq = m_rgb
        
        if(not isinstance(yiq, type(None))):
            w = yiq.shape[0]
            h = yiq.shape[1]
            p=3
            rgb = np.zeros((w,h,p))
            #m_yiq.shape
            rgb[:,:,0] = 1 * yiq[:,:,0] + 0.9663 * yiq[:,:,1] + 0.6210 * yiq[:,:,2]
            rgb[:,:,1] = 1 * yiq[:,:,0] + -0.2721 * yiq[:,:,1] + -0.6474 * yiq[:,:,2]
            rgb[:,:,2] = 1 * yiq[:,:,0] + -1.1070 * yiq[:,:,1] + 1.7046 * yiq[:,:,2]
            
            rgb = np.clip(rgb,0.,1.)
    
            """ Grafico de la imagen en el espacio RGB """
            
            fig = Figure(figsize = (3, 3), dpi = 100)
            plot = fig.add_subplot()
            plot.set_title(titulo)
            plot.imshow(rgb)
            
            self.canvas = FigureCanvasTkAgg(fig, master=window)   
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(column=8, row=0, columnspan=3, rowspan=4, padx=(10,10), pady=(10,10))
        else:
            print('Primero debe pasar RGB a YIQ')
        
    def cambiar_luminancia(self):
        self.value = float(self.lum.get())
        m_yiq = self.file_yiq.copy()
        m_y_yiq = m_yiq[:,:,0]*self.value
        m_yiq[:,:,0] = m_y_yiq
        
        self.yiq_to_rgb(m_yiq, 'Luminosidad Modificada');
        
    def cambiar_crominancia(self):
        self.value = float(self.crom.get())
        m_yiq = self.file_yiq.copy()
        m_i_yiq = m_yiq[:,:,1]*self.value
        m_q_yiq = m_yiq[:,:,2]*self.value
        m_yiq[:,:,1] = m_i_yiq
        m_yiq[:,:,2] = m_q_yiq
        
        self.yiq_to_rgb(m_yiq, 'Saturacion Modificada');
  
window = tk.Tk()  
window.title('Trabajo Practico N1')
window.geometry("1080x600")
width= window.winfo_screenwidth()
height= window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))

app = Application(master=window)
  
app.mainloop()