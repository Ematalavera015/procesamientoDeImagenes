# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 01:02:00 2022

@author: Ema Talavera
"""
import tkinter as tk
from tkinter import filedialog , messagebox, ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import imageio.v2 as imageio
import numpy as np


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.methods = None
        self.file = None
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
        self.methods = ("RGB to YIQ","YIQ to RGB")
        
        self.quit = tk.Button(window, text="QUIT", fg="red", command=window.destroy)
        self.quit.place(x=100, y=10, width=100, height=30)
        self.quit.pack(side="bottom")
        
        self.plot_button = tk.Button(window, command = self.open_file, height = 2, width = 10, text = "Abrir Imagen")
        self.plot_button.place(x=0, y=10, width=100, height=30)
        self.plot_button.pack()
        
        # if(self.file != None):
        #     # create a Combobox with themes to choose from
        #     self.combo = ttk.Combobox(window, values=self.methods)
        #     self.combo.pack(padx=32, pady=8)
        #     # make the Enter key change the style
        #     #self.combo.bind('<Return>', self.change_style)
        #     # make a Button to change the style
        #     self.combo_button = tk.Button(window, text='OK')
        #     self.combo_button['command'] = self.change_space
        #     self.combo_button.pack(pady=8)

    def change_space(self, event=None):
        
        space = self.combo.get()
        try:
            print("Metodo elegido ", space)
            if("RGB to YIQ"==space):
                print('Cambiar a YIQ')
                self.rgb_to_yiq()
            else:
                print('Cambiar a RGB')
                self.yiq_to_rgb()()
        except tk.TclError as err:
            messagebox.showerror('Error', err)
        else:
            window.title(space)
        
        
    def open_file(self):
        archivo = filedialog.askopenfilename(title="abrir", initialdir="C:/", filetypes = (("Archivos png", "*.png"), ("Todos lod archivos", "*.*")))
        if archivo:
            rgb = imageio.imread(archivo)/255.
            
            self.file = np.array(rgb)
            self.plot(rgb)
            self.combo = ttk.Combobox(window, values=self.methods)
            self.combo.pack(padx=32, pady=8)
            
            # boton cambiar espacio
            self.combo_button = tk.Button(window, text='Aceptar')
            self.combo_button['command'] = self.change_space
            self.combo_button.pack(pady=8)
            # boton limpiar
            # self.clean_button = tk.Button(window, text='Limpiar')
            # self.clean_button['command'] = self.clean_plot
            # self.clean_button.pack(pady=8)
            
       
  
    def plot(self, file):
        
        fig = Figure(figsize = (2, 2), dpi = 100)
        plot = fig.add_subplot()
        plot.set_title('Imagen RGB')
        plot.imshow(file) 
        canvas = FigureCanvasTkAgg(fig, master = window)   
        canvas.draw() 
        canvas.get_tk_widget().pack() 
        # toolbar = NavigationToolbar2Tk(canvas, window) 
        # toolbar.update() 
        # canvas.get_tk_widget().pack()
    
    def clean_plot():
        print('limpiar')
    
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

        self.plot(yiq)
    
    def yiq_to_rgb(self):
        w = self.file.shape[0]
        h = self.file.shape[1]
        p=3
        rgb = np.zeros((w,h,p))
        #m_yiq.shape
        rgb[:,:,0] = 1 * self.file[:,:,0] + 0.9663 * self.file[:,:,1] + 0.6210 * self.file[:,:,2]
        rgb[:,:,1] = 1 * self.file[:,:,0] + -0.2721 * self.file[:,:,1] + -0.6474 * self.file[:,:,2]
        rgb[:,:,2] = 1 * self.file[:,:,0] + -1.1070 * self.file[:,:,1] + 1.7046 * self.file[:,:,2]
        
        rgb = np.clip(rgb,0.,1.)

        self.plot(rgb)
  
window = tk.Tk() 
  
window.title('Trabajo Practico N1') 
  
#window.geometry("1080x600")
width= window.winfo_screenwidth()  
height= window.winfo_screenheight() 
window.geometry("%dx%d" % (width-200, height-150))
  
app = Application(master=window)
  
app.mainloop() 