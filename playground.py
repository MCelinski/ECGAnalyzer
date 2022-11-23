import tkinter.messagebox
import customtkinter
import matplotlib
from matplotlib import image
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
import os
import tkinter as tk
import tkinter.filedialog
import scipy.signal as signal
import scipy.fftpack  
import matplotlib.pyplot
import numpy as np
import wfdb
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from scipy import signal
from wfdb import processing

PATH = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  
customtkinter.deactivate_automatic_dpi_awareness()

class App(customtkinter.CTk):
    WIDTH = 1600
    HEIGHT = 900
    def __init__(self):
        super().__init__()
        self.title("Program do wyświetlania sygnałów ECG")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  
        self.step = tk.IntVar(master=self,value=0)
        
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
        
        # self.frame_right = customtkinter.CTkFrame(master=self)
        # self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        self.add_file_image = self.load_image("/images/add-folder.png", 20)
        self.add_anotate_image = self.load_image("/images/anotate2.png", 20)
        self.add_analyze_image =self.load_image("/images/tools-icon.png",20)
        self.add_heart_image = self.load_image("/images/ecgg.png",120)
        self.add_info_image = self.load_image("/images/fileinfo.png",20)
        self.add_xmark_image = self.load_image("/images/xmark.png",20)
        self.add_left_arrow = self.load_image("/images/arrowleft.png",50)
        self.add_right_arrow = self.load_image("/images/arrowright.png",50)
        self.add_list_view = self.load_image("/images/listview.png",20)
        self.add_addannotation_image =self.load_image("/images/addnewanotation.png",20)
        
        self.step = tk.IntVar()
        

 
        self.label_1 = customtkinter.CTkButton(master=self.frame_left,image=self.add_heart_image,compound="bottom", 
                                                corner_radius=10,
                                                text="ECG Analyzer",text_font=("Roboto Medium", -20))
        self.label_1.grid(row=0, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,image=self.add_file_image,compound="right",
                                                text="Wczytaj dane     ",command=self.read_data
                                                )
        self.button_1.grid(row=1, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,image=self.add_anotate_image,compound="right",
                                                text="Wczytaj anotacje ",command=self.readannotation)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)
        
        self.button_7 = customtkinter.CTkButton(master=self.frame_left,image=self.add_addannotation_image,compound="right",
                                                text="Dodaj anotacje   ",command=self.AddAnotation)
        self.button_7.grid(row=3, column=0, pady=10, padx=20)
        
        
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,image=self.add_analyze_image,compound="right", 
                                                text="Analizuj sygnał     ",command=self.analize_signal)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)
        
        self.button_4 = customtkinter.CTkButton(master=self.frame_left,image=self.add_info_image,compound="right", 
                                                text="informacje o pliku",command=self.show_info)
        self.button_4.grid(row=5, column=0, pady=10, padx=20)  
        
        self.button_5 = customtkinter.CTkButton(master=self.frame_left,image=self.add_left_arrow,compound="right", 
                                                text="",text_font=("Roboto Medium", -12),command=self.left_arrow)
        self.button_5.grid(row=9, column=0, pady=10, padx=20)  
        
        self.button_6 = customtkinter.CTkButton(master=self.frame_left,image=self.add_right_arrow,compound=tk.CENTER,
                                                text="",text_font=("Roboto Medium", -12),command=self.right_arrow)
        self.button_6.grid(row=8, column=0, pady=10, padx=20)  
        
        self.optionmenu_2 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Widok Kaskadowy", "Widok Pojedynczy"],
                                                        command=self.change_view_mode)
        self.optionmenu_2.grid(row=7, column=0, pady=10, padx=20, sticky="w")
        
        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=11, column=0, pady=10, padx=20, sticky="w")
        
    
    def right_arrow(self):
              self.toolbar.pack_forget()
              self.step.set(self.step.get() +3000)
              self.readRecords()
        
         
    def left_arrow(self):
              self.toolbar.pack_forget()
              self.step.set(self.step.get() -3000)
              self.readRecords()
        
        
    def change_view_mode(self,view):
        
        if view == "Widok Pojedynczy":
            self.single_view()
        else:
            self.cascade_view()
        
        
    def single_view(self):
        try:
             self.frame_right.pack_forget()
             self.frame_info.pack_forget()
             self.frame_info1.pack_forget()
             self.frame_info2.pack_forget()
        except AttributeError:
              pass
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=30)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=8, pady=20, padx=20, sticky="nsew")
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        self.frame_info.config
        

    def cascade_view(self):
        try:
             self.frame_right.pack_forget()
             self.frame_info.pack_forget()
             self.frame_info1.pack_forget()
             self.frame_info2.pack_forget()
        except AttributeError:
              pass
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.frame_right.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.frame_right.columnconfigure((0, 1), weight=1)
        
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=2, pady=10, padx=10, sticky="nsew")
        
        self.frame_info1 = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info1.grid(row=2, column=0, columnspan=2, rowspan=2, pady=10, padx=10, sticky="nsew")
        
        self.frame_info2 = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info2.grid(row=4, column=0, columnspan=2, rowspan=2, pady=10, padx=10, sticky="nsew")
      

        # ============ frame_info ============

    
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        self.frame_info.config
        
        self.frame_info1.rowconfigure(0, weight=1)
        self.frame_info1.columnconfigure(0, weight=1)
        self.frame_info1.config
        
        self.frame_info2.rowconfigure(0, weight=1)
        self.frame_info2.columnconfigure(0, weight=1)
        self.frame_info2.config

        
    def read_data(self):
        global ecg_path
        global addSamples
        ecg_path = tkinter.filedialog.askopenfilename()
        ecg_path = ecg_path[:-4]
        input = customtkinter.CTkInputDialog(self, text="Ile próbek wyświetlić\nWpisz '0' aby wyświetlić cały sygnał: ", title="Ilość próbek do wyświetlenia")
        self.getedinput=int(input.get_input())
        self.readRecords()
        
    def readRecords(self):
        global fields
        
        signals, fields = wfdb.rdsamp(ecg_path,sampfrom=  self.step.get() , sampto = self.getedinput + self.step.get(),
                                  channels=[0])
        
        self.record1 = wfdb.rdrecord(ecg_path,sampfrom=  self.step.get() , sampto = self.getedinput + self.step.get(),
                                channels=[0])
        
        self.record2 = wfdb.rdrecord(ecg_path, sampfrom =  self.getedinput + self.step.get(), sampto=  2 * self.getedinput + self.step.get(),
                                channels=[0])
        
        self.record3 = wfdb.rdrecord(ecg_path,sampfrom = 2 * self.getedinput + self.step.get(), sampto= 3 * self.getedinput + self.step.get(),
                                channels=[0])
        
        self.annotation = wfdb.rdann(ecg_path, 'atr', self.step.get() , sampto = self.getedinput + self.step.get(),shift_samps=True)
        # self.annotation_Info = wfdb.rdann(ecg_path, 'atr',sampto=300000)
        self.DrawSignals()
    
    def DrawSignals(self):
        try:
              self.canvas.get_tk_widget().pack_forget()
              self.canvas1.get_tk_widget().pack_forget()
              self.canvas2.get_tk_widget().pack_forget()
              self.toolbar.pack_forget()
              self.toolbar1.pack_forget()
              self.toolbar2.pack_forget()
        except AttributeError:
              pass
        figure_time =str(round((self.getedinput + self.step.get())/self.record1.fs,0)) 
        return_fig = wfdb.plot_wfdb( record=self.record1,plot_sym=True,title = f"file:{ecg_path[-8:]} Time: {round(self.step.get()/self.record1.fs,0)}s -{figure_time}s",
                    time_units='seconds',
                    figsize=(2,2), ecg_grids='all',return_fig=True)
        return_fig.set_facecolor("#F2F2F2")
        
        figure1_time =str(round((2*self.getedinput + self.step.get())/self.record1.fs,0)) 
        return_fig1 = wfdb.plot_wfdb( record=self.record2,plot_sym=True,title=f"file: {ecg_path[-8:]}  Time: {figure_time}s -{figure1_time}s",
                    time_units='seconds',
                    figsize=(2,2), ecg_grids='all',return_fig=True,)
        return_fig1.set_facecolor("#F2F2F2")
        
        figure2_time =str(round((3*self.getedinput + self.step.get())/self.record1.fs,0)) 
        return_fig2 = wfdb.plot_wfdb( record=self.record3,plot_sym=True,title=f"file: {ecg_path[-8:]}  Time: {figure1_time} s- {figure2_time}s",
                    time_units='seconds',
                    figsize=(2,2), ecg_grids='all',return_fig=True)
        return_fig2.set_facecolor("#F2F2F2")
        
        
        self.canvas = FigureCanvasTkAgg(return_fig,master=self.frame_info)
        self.canvas.draw() 
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_info)
        self.toolbar.config(background="#F2F2F2")
 
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
        
        self.canvas1 = FigureCanvasTkAgg(return_fig1,master=self.frame_info1)
        self.canvas1.draw() 
        self.canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
       
        self.toolbar1 = NavigationToolbar2Tk(self.canvas1, self.frame_info1)
        self.toolbar1.config(background="#F2F2F2")
        self.toolbar1.update()
        self.canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
        
        self.canvas2 = FigureCanvasTkAgg(return_fig2,master=self.frame_info2)
        self.canvas2.draw() 
        self.canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.frame_info2)
        self.toolbar2.config(background="#F2F2F2")
        self.toolbar2.update()
        self.canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)     
        
    def readannotation(self):
        try:
              self.canvas.get_tk_widget().pack_forget()
              self.toolbar.pack_forget()
              
              self.canvas1.get_tk_widget().pack_forget()
              self.toolbar1.pack_forget()
              
              self.canvas2.get_tk_widget().pack_forget()
              self.toolbar2.pack_forget()
              
              self.canvas3.get_tk_widget().pack_forget()
              self.toolbar3.pack_forget()
        except AttributeError:
              pass
        figure_time =str(round((self.getedinput + self.step.get())/self.record1.fs,0)) 
        self.return_figwithann = wfdb.plot_wfdb( record=self.record1, annotation=self.annotation,plot_sym=True,
                    time_units='seconds', title = f"file:{ecg_path[-8:]} Time: {round(self.step.get()/self.record1.fs,0)}s -{figure_time}s",
                    figsize=(10,6), ecg_grids='all',return_fig=True)
        
        self.canvas = FigureCanvasTkAgg(self.return_figwithann,master=self.frame_info)
        self.canvas.draw() 
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_info)
        self.toolbar.config(background="#F2F2F2")
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
    
    def AddAnotation(self):
        
        annotation = customtkinter.CTkToplevel(self)
        annotation.geometry("600x200")
        annotation.title("Dodaj Anotacje")
        annotation.grid_columnconfigure(1, weight=1)
        annotation.grid_rowconfigure(0, weight=1)
 
        annotation.frame_left = customtkinter.CTkFrame(master=annotation,
                                                 width=60,
                                                 corner_radius=0)
        annotation.frame_left.grid(row=0, column=0, sticky="nswe")
 
         # ============ frame_left ============

        # configure grid layout (1x11)
        annotation.frame_left.grid_rowconfigure(0, minsize=5)   # empty row with minsize as spacing
        annotation.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        annotation.frame_left.grid_rowconfigure(8, minsize=10)    # empty row with minsize as spacing
        
        annotation.frame_left.grid_rowconfigure(11, minsize=5)  # empty row with minsize as spacing
        annotation.add_annotation_image =self.load_image("/images/anotate2.png",40)
        annotation.add_addannotation_image =self.load_image("/images/addnewanotation.png",25)
        annotation.frame_right = customtkinter.CTkFrame(master=annotation)
        annotation.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        annotation.label_1 = customtkinter.CTkButton(master=annotation.frame_left,image=annotation.add_annotation_image,compound="bottom", 
                                                corner_radius=10,
                                                text="",text_font=("Roboto Medium", -20))
        annotation.label_1.grid(row=5, column=0, pady=10, padx=10)
        
        annotation.label_1 = customtkinter.CTkButton(master=annotation.frame_left,image=annotation.add_annotation_image,compound="bottom", 
                                                corner_radius=10,
                                                text="",text_font=("Roboto Medium", -20))
        annotation.label_1.grid(row=5, column=0, pady=10, padx=10)
            
        annotation.label_info_1 = customtkinter.CTkLabel(master=annotation.frame_right,
                                                   text="Próbka czasowa:",
                                                   height=10,
                                                   corner_radius=6,  
                                                   fg_color=("white", "gray38"),  
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        annotation.label_info_1.grid(column=1, row=0, sticky="nwe", padx=5, pady=5)
        
        annotation.entry1 = customtkinter.CTkEntry(master=annotation.frame_right,
                                            width=120,
                                            placeholder_text="Podaj czas")
        annotation.entry1.grid(row=0, column=2, columnspan=2, sticky="we")
        
        
        annotation.label_info_2 = customtkinter.CTkLabel(master=annotation.frame_right,
                                                   text="Symbol anotacji:",
                                                   height=10,
                                                   corner_radius=6,  
                                                   fg_color=("white", "gray38"),  
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        annotation.label_info_2.grid(column=1, row=1, sticky="nwe", padx=5, pady=5)
        
        annotation.entry2 = customtkinter.CTkEntry(master=annotation.frame_right,
                                            width=120,
                                            placeholder_text="Podaj symbol")
        annotation.entry2.grid(row=1, column=2, columnspan=2, sticky="we")
        
        def getValues():
            ann_sample = float(annotation.entry1.get())
            new_symbol = str(annotation.entry2.get())
            ann_sample = self.record1.fs * ann_sample
            nearest_min =np.where(self.annotation.sample == self.annotation.sample[self.annotation.sample > ann_sample].min())
            index = nearest_min[0][0]
            self.annotation.symbol.insert(index,new_symbol)
            self.annotation.sample = np.insert(self.annotation.sample,index,ann_sample)
            annotation.destroy()
        
        annotation.button_2 = customtkinter.CTkButton(master=annotation.frame_right,image=annotation.add_addannotation_image,compound="bottom", 
                                                corner_radius=10,
                                                text="Dodaj nową anotacje: ",text_font=("Roboto Medium", -20),command =getValues )
        annotation.button_2.grid(row=2, column=1, pady=10, padx=10)
        
        
       
        
        wfdb.wrann("104v2",'atr',self.annotation.sample,self.annotation.symbol)

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
                                                   text=f"częsotliwość próbkowania: {self.record1.fs} [Hz]",
                                                   height=10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT,
                                                   anchor="center",
                                                   text_font=("Trebuchet MS",12))
        window.label_info_1.grid(column=1, row=0, sticky="nwe", padx=5, pady=5)
        
        window.label_info_2 = customtkinter.CTkLabel(master=window.frame_right,
                                                   text=f"Długość sygnału: {round(self.record1.sig_len/self.record1.fs,2)}[s]",
                                                   height=10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT,
                                                   anchor="w",
                                                   text_font=("Trebuchet MS",12))
        window.label_info_2.grid(column=1, row=1, sticky="nwe", padx=5, pady=5)
        
        window.label_info_3 = customtkinter.CTkLabel(master=window.frame_right,
                                                   text=f"Liczba Próbek: {round(self.record1.sig_len)}",
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
        analyze.add_filter_image =self.load_image("/images/filter.png",20)
        analyze.frame_right = customtkinter.CTkFrame(master=analyze)
        analyze.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        analyze.label_1 = customtkinter.CTkButton(master=analyze.frame_left,image=analyze.add_analyze_image,compound="bottom", 
                                                corner_radius=10,
                                                text="Analiza sygnału",text_font=("Roboto Medium", -20))
        analyze.label_1.grid(row=5, column=0, pady=10, padx=10)
        
        rr_array = wfdb.ann2rr(ecg_path, 'atr', as_array=True,format='s',stop_time=self.record1.sig_len)
        mean_rr = np.mean(rr_array)
        mean_hr = processing.calc_mean_hr(rr_array,rr_units='seconds')
    
        def FFTfilter():
            try:
                self.canvas.get_tk_widget().pack_forget()
                self.toolbar.pack_forget()
                
                self.canvas1.get_tk_widget().pack_forget()
                self.toolbar1.pack_forget()
                
                self.canvas2.get_tk_widget().pack_forget()
                self.toolbar2.pack_forget()
                
                self.canvas3.get_tk_widget().pack_forget()
                self.toolbar3.pack_forget()
            except AttributeError:
                pass
            arr1 = [] 
            for x in self.record1.p_signal:        
                arr1.extend(x)      
                data = list(arr1)
            b, a = scipy.signal.butter(3, 0.1)
            filtered = scipy.signal.filtfilt(b, a, data)
            self.record1.p_signal = filtered
            
            arr2 = [] 
            for x in self.record2.p_signal:        
                arr2.extend(x)      
                data = list(arr2)
            b, a = scipy.signal.butter(3, 0.1)
            filtered = scipy.signal.filtfilt(b, a, data)
            self.record2.p_signal = filtered
            
            arr3=[]
            for x in self.record3.p_signal:        
                arr3.extend(x)      
                data = list(arr3)
            b, a = scipy.signal.butter(3, 0.1)
            filtered = scipy.signal.filtfilt(b, a, data)
            self.record3.p_signal = filtered

            self.DrawSignals()
            
            analyze.destroy()
        
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
        
        analyze.button_2 = customtkinter.CTkButton(master=analyze.frame_right,image=analyze.add_filter_image,compound="bottom", 
                                                corner_radius=10,
                                                text="Zastosuj filtr FFT: ",text_font=("Roboto Medium", -20),command=FFTfilter)
        analyze.button_2.grid(row=2, column=1, pady=5, padx=5)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
    