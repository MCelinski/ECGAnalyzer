
from re import A
import tkinter.messagebox
import customtkinter
from  PIL import Image, ImageTk
import matplotlib
from matplotlib import image
matplotlib.use("TkAgg")
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
import numpy as np
import tkinter as tk
import tkinter.filedialog
import os
import wfdb
from wfdb import processing
import pandas as pd
from scipy import signal

PATH = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  
customtkinter.deactivate_automatic_dpi_awareness()

class App(customtkinter.CTk):

    WIDTH = 1224
    HEIGHT = 720
    def __init__(self):
        super().__init__()
        self.title("Program do wyświetlania sygnałów ECG")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
 
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=60,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
 
         # ============ frame_left ============

        self.frame_left.grid_rowconfigure(0, minsize=10)   
        self.frame_left.grid_rowconfigure(6, weight=1)  
        self.frame_left.grid_rowconfigure(8, minsize=20)    
        self.frame_left.grid_rowconfigure(11, minsize=10)  
        
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        self.add_file_image = self.load_image("/images/add-folder.png", 20)
        self.add_anotate_image = self.load_image("/images/anotate2.png", 20)
        self.add_analyze_image =self.load_image("/images/tools-icon.png",20)
        self.add_heart_image = self.load_image("/images/ecgg.png",120)
        self.add_info_image = self.load_image("/images/fileinfo.png",20)
        self.add_xmark_image = self.load_image("/images/xmark.png",20)
        

 
        self.label_1 = customtkinter.CTkButton(master=self.frame_left,image=self.add_heart_image,compound="bottom", 
                                                corner_radius=10,
                                                text="ECG Analyzer",text_font=("Roboto Medium", -20))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,image=self.add_file_image,compound="right",
                                                text="Wczytaj dane   ",command=self.read_data
                                                )
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,image=self.add_anotate_image,compound="right",
                                                text="Dodaj anotacje ",command=self.readannotation)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)
        
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,image=self.add_analyze_image,compound="right", 
                                                text="Analizuj sygnał     ",command=self.analize_signal)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)
        
        self.button_4 = customtkinter.CTkButton(master=self.frame_left,image=self.add_info_image,compound="right", 
                                                text="informacje o pliku",command=self.show_info)
        self.button_4.grid(row=5, column=0, pady=10, padx=20)  

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

               
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=30)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=8, pady=20, padx=20, sticky="nsew")
        

        # ============ frame_info ============

    
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        self.frame_info.config
        
    def read_data(self):
        try:
              self.canvas.get_tk_widget().pack_forget()
              self.toolbar.pack_forget()
        except AttributeError:
              pass
        global ecg_path
        global signalSample
        global fields
        global annotation
        global record
        ecg_path = tkinter.filedialog.askopenfilename()
        ecg_path = ecg_path[:-4]

        
        input = customtkinter.CTkInputDialog(self, text="Ile próbek wyświetlić\nWpisz '0' aby wyświetlić cały sygnał: ", title="Ilość próbek do wyświetlenia")
        getedinput= input.get_input()
        if getedinput == 'all':
            signalSample,fields = wfdb.rdsamp(ecg_path, warn_empty=True,channels=[0])        
            record = wfdb.rdrecord(ecg_path,channels=[0])
            annotation = wfdb.rdann(ecg_path, 'atr')
        else:    
            
            signalSample,fields = wfdb.rdsamp(ecg_path,sampto = int(getedinput),channels=[0], warn_empty=True)   
            record = wfdb.rdrecord(ecg_path, sampto=int(getedinput),channels=[0])
            annotation = wfdb.rdann(ecg_path, 'atr', sampto=int(getedinput))

        return_fig = wfdb.plot_wfdb( record=record,plot_sym=True,
                    time_units='seconds', title=ecg_path,
                    figsize=(10,6), ecg_grids='all',return_fig=True)
        return_fig.set_facecolor("#F2F2F2")
        
        self.canvas = FigureCanvasTkAgg(return_fig,master=self.frame_info)
        self.canvas.draw() 
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_info)
        self.toolbar.config(background="#F2F2F2")
 
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
    
    def readannotation(self):
        try:
              self.canvas.get_tk_widget().pack_forget()
              self.toolbar.pack_forget()
        except AttributeError:
              pass
        self.return_figwithann = wfdb.plot_wfdb( record=record, annotation=annotation,plot_sym=True,
                    time_units='seconds', title=ecg_path,
                    figsize=(10,6), ecg_grids='all',return_fig=True)
        self.canvas = FigureCanvasTkAgg(self.return_figwithann,master=self.frame_info)
        self.canvas.draw() 
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_info)
        self.toolbar.config(background="#F2F2F2")
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
    def on_closing(self, event=0):
        self.quit()
        
    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def load_image(self, path, image_size):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def show_info(self):
        
    
        window = customtkinter.CTkToplevel(self)
        window.geometry("600x200")
        window.title("Informacje o pliku")
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(0, weight=1)
 
        window.frame_left = customtkinter.CTkFrame(master=window,
                                                 width=60,
                                                 corner_radius=0)
        window.frame_left.grid(row=0, column=0, sticky="nswe")
 
         # ============ frame_left ============

        # configure grid layout (1x11)
        window.frame_left.grid_rowconfigure(0, minsize=5)   # empty row with minsize as spacing
        window.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        window.frame_left.grid_rowconfigure(8, minsize=10)    # empty row with minsize as spacing
        window.frame_left.grid_rowconfigure(11, minsize=5)  # empty row with minsize as spacing
        
        window.frame_right = customtkinter.CTkFrame(master=window)
        window.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        window.add_file_image = self.load_image("/images/filepropt.png", 40)
        window.label_1 = customtkinter.CTkButton(master=window.frame_left,image=window.add_file_image,compound="bottom", 
                                                corner_radius=10,
                                                text="informacje o pliku",text_font=("Roboto Medium", -20))
        window.label_1.grid(row=5, column=0, pady=10, padx=10)
        
        
        
        comment = fields['comments'][0]
        age = comment[0:2]
        gender = comment[3]
        
        if age == "-1":
            age ="brak informacji"
        if gender == "M":
            gender ="Mężczyzna"
        elif gender =="F":
            gender ="Kobieta"
        else:
            gender="Brak Informacji"
            
            
        window.label_info_1 = customtkinter.CTkLabel(master=window.frame_right,
                                                   text=f"częsotliwość próbkowania: {fields['fs']} [Hz]",
                                                   height=10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT,
                                                   anchor="center",
                                                   text_font=("Trebuchet MS",12))
        window.label_info_1.grid(column=1, row=0, sticky="nwe", padx=5, pady=5)
        
        window.label_info_2 = customtkinter.CTkLabel(master=window.frame_right,
                                                   text=f"Długość sygnału: {round(record.sig_len/record.fs,2)}[s]",
                                                   height=10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        window.label_info_2.grid(column=1, row=1, sticky="nwe", padx=5, pady=5)
        
        window.label_info_3 = customtkinter.CTkLabel(master=window.frame_right,
                                                   text=f"Liczba Próbek: {round(record.sig_len)}",
                                                   height=10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        window.label_info_3.grid(column=1, row=2, sticky="nwe", padx=5, pady=5)
        
        window.label_info_3 = customtkinter.CTkLabel(master=window.frame_right,
                                                   text=f"Wiek: {age}",
                                                   height=10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        window.label_info_3.grid(column=1, row=2, sticky="nwe", padx=5, pady=5)
        
        window.label_info_3 = customtkinter.CTkLabel(master=window.frame_right,
                                                   text=f"Płeć: {gender}",
                                                   height=10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        window.label_info_3.grid(column=1, row=3, sticky="nwe", padx=5, pady=5)
   
   
    def analize_signal(self):
        analyze = customtkinter.CTkToplevel(self)
        analyze.geometry("600x200")
        analyze.title("Analiza sygnału")
        analyze.grid_columnconfigure(1, weight=1)
        analyze.grid_rowconfigure(0, weight=1)
 
        analyze.frame_left = customtkinter.CTkFrame(master=analyze,
                                                 width=60,
                                                 corner_radius=0)
        analyze.frame_left.grid(row=0, column=0, sticky="nswe")
 
         # ============ frame_left ============

        # configure grid layout (1x11)
        analyze.frame_left.grid_rowconfigure(0, minsize=5)   # empty row with minsize as spacing
        analyze.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        analyze.frame_left.grid_rowconfigure(8, minsize=10)    # empty row with minsize as spacing
        analyze.frame_left.grid_rowconfigure(11, minsize=5)  # empty row with minsize as spacing
        analyze.add_analyze_image =self.load_image("/images/tools-icon.png",40)
        analyze.frame_right = customtkinter.CTkFrame(master=analyze)
        analyze.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        analyze.label_1 = customtkinter.CTkButton(master=analyze.frame_left,image=analyze.add_analyze_image,compound="bottom", 
                                                corner_radius=10,
                                                text="Analiza sygnału",text_font=("Roboto Medium", -20))
        analyze.label_1.grid(row=5, column=0, pady=10, padx=10)
        
        
        rr_array = wfdb.ann2rr(ecg_path, 'atr', as_array=True,format='s',stop_time=record.sig_len)
        mean_rr = np.mean(rr_array)
        mean_hr = processing.calc_mean_hr(rr_array,rr_units='seconds')
        
        qrs_inds = wfdb.processing.xqrs_detect(signalSample[:,0], fields['fs'], sampfrom=0, sampto=record.sig_len, conf=None, learn=True, verbose=True)

        

            
            
        analyze.label_info_1 = customtkinter.CTkLabel(master=analyze.frame_right,
                                                   text=f"Odstęp R-R:\n Max:{round(rr_array.max(),2)} [s] Min:{round(rr_array.min(),2)} [s] Mean:{round(mean_rr,2)} [s]",
                                                   height=10,
                                                   corner_radius=6,  
                                                   fg_color=("white", "gray38"),  
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        analyze.label_info_1.grid(column=1, row=0, sticky="nwe", padx=5, pady=5)
        
        analyze.label_info_2 = customtkinter.CTkLabel(master=analyze.frame_right,
                                                   text=f"Średnie HR: {round(mean_hr,3)}[Bpm]",
                                                   height=10,
                                                   corner_radius=6, 
                                                   fg_color=("white", "gray38"),  
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        analyze.label_info_2.grid(column=1, row=1, sticky="nwe", padx=5, pady=5)
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
    