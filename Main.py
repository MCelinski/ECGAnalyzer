
from re import A
import tkinter.messagebox
import customtkinter
from  PIL import Image, ImageTk
import matplotlib
from matplotlib import image
matplotlib.use("TkAgg")
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import numpy as np
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
import os
import wfdb
import pandas as pd
from scipy import signal

PATH = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.deactivate_automatic_dpi_awareness()

class App(customtkinter.CTk):

    WIDTH = 1024
    HEIGHT = 720
    def __init__(self):
        super().__init__()
        self.title("Program do wyświetlania sygnałów ECG")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
 
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=60,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
 
         # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        self.add_file_image = self.load_image("/images/add-folder.png", 20)
        self.add_anotate_image = self.load_image("/images/anotate2.png", 20)
        self.add_analyze_image =self.load_image("/images/tools-icon.png",20)
        self.add_heart_image = self.load_image("/images/ecgg.png",120)
        self.add_info_image = self.load_image("/images/fileinfo.png",20)
        

 
        self.label_1 = customtkinter.CTkButton(master=self.frame_left,image=self.add_heart_image,compound="bottom", 
                                                corner_radius=10,
                                                text="ECG Analyzer",text_font=("Roboto Medium", -20))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,image=self.add_file_image,compound="right",
                                                text="Wczytaj dane   ",command=self.read_data
                                                )
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,image=self.add_anotate_image,compound="right",
                                                text="Dodaj anotacje ",)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)
        
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,image=self.add_analyze_image,compound="right", 
                                                text="Filtruj sygnał      ",)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)
        
        self.button_4 = customtkinter.CTkButton(master=self.frame_left,image=self.add_info_image,compound="right", 
                                                text="informacje o pliku",command=self.show_info)
        self.button_4.grid(row=4, column=0, pady=10, padx=20)  
        
        
        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")
               
                # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=30)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")
        
        


        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        self.frame_info.config
        
    def read_data(self):
        global signalSample
        global fields
        global ann
        ecg_path = tkinter.filedialog.askopenfilename()
        ecg_path = ecg_path[:-4]
        
        input = customtkinter.CTkInputDialog(self, text="Ile próbek wyświetlić: ", title="Ilość próbek do wyświetlenia")
        n_samples = int(input.get_input())
        chanels=[1]
        
        record = wfdb.rdrecord(ecg_path, sampto=n_samples,channels=chanels)
        annotation = wfdb.rdann(ecg_path, 'atr', sampto=3000)

        return_fig = wfdb.plot_wfdb( record=record, annotation=annotation, plot_sym=True,
        time_units='seconds', title='MIT-BIH Record 100',
        figsize=(10,6), ecg_grids='all',return_fig=True)
        return_fig.set_facecolor("#F2F2F2")
    
        
        

        
        
        
        #   n_samples = tkinter.simpledialog.askinteger('Liczba próbek', 
        # 	# 'Wpisz ile próbek chcesz wyświetlić(przykład: 3000, 6000, 10000 etc.)')

        # signalSample,fields = wfdb.rdsamp(ecg_path,sampto = n_samples,channels=[0], warn_empty=True)
        # signal_list = signalSample.tolist()
        
        # ann = wfdb.rdann(ecg_path, 'dat', sampto=n_samples)
        # annotation_time = (ann.sample / ann.fs)
        # ann_sample = (ann.sample)
        # ann_symbols = (ann.symbol)
        # fs = fields.get('fs')      
        # time =np.arange(n_samples) /fs
       
        # self.color =self.change_appearance_mode 
        # f = Figure(figsize=(10,6), dpi=100,facecolor="#F2F2F2")
        # a = f.add_subplot(111)
        
        # a.set_xlabel("time in s")
        # a.set_ylabel("ECG in mV")
        # a.set_title("ECG Signal")
        # a.set_xlim(0, 10)
        # a.grid()
        # a.set_facecolor('#F2F2F2')
        # a.plot(time,signal_list,'r')
    

        
        self.canvas = FigureCanvasTkAgg(return_fig,master=self.frame_info)
        
        self.canvas.draw()
        
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_info)
        self.toolbar.config(background="#F2F2F2")

        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # self.cursor = Cursor(a, horizOn=True, vertOn=True, useblit=True, color = 'r', linewidth = 1)
        # annot = a.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points",
        #                 bbox=dict(boxstyle='round4', fc='linen',ec='k',lw=1),
        #                 arrowprops=dict(arrowstyle='-|>'))
        # annot.set_visible(False)
        # self.coord = []
        # signalSample.Get()
        # fields.Get()
        # ann.Get()
                
    def on_closing(self, event=0):
        self.destroy()
        
    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def show_info(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")
        window.title("Informacje o pliku")
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(0, weight=1)
 
        window.frame_left = customtkinter.CTkFrame(master=window,
                                                 width=60,
                                                 corner_radius=0)
        window.frame_left.grid(row=0, column=0, sticky="nswe")
 
         # ============ frame_left ============

        # configure grid layout (1x11)
        window.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        window.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        window.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        window.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        
        window.frame_right = customtkinter.CTkFrame(master=window)
        window.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        window.add_file_image = self.load_image("/images/filepropt.png", 40)
        window.add_anotate_image = self.load_image("/images/anotate2.png", 20)
    
        

 
        window.label_1 = customtkinter.CTkButton(master=window.frame_left,image=window.add_file_image,compound="bottom", 
                                                corner_radius=10,
                                                text="informacje o pliku",text_font=("Roboto Medium", -20))
        window.label_1.grid(row=1, column=0, pady=10, padx=10)
        
        # window.grid_columnconfigure(1, weight=1)
        # window.grid_rowconfigure(0, weight=1)
        # window.add_heart_image = self.load_image("/images/ecgg.png",30)
        # text_var = tkinter.StringVar(value="częstość próbkowania:")
        # window.label_1 = customtkinter.CTkButton(window,image=self.add_heart_image,compound="bottom", 
        #                                         corner_radius=10,
        #                                         text="ECG Analyzer",text_font=("Roboto Medium", -20))
        # window.label_1.grid(row=1, column=0, pady=10, padx=10)

        # create label on CTkToplevel window
        # label = customtkinter.CTkLabel(window, text="Informacje o pliku")
        # label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        # print(signalSample)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    