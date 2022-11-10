import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.figure import Figure

import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.filedialog

from math import pi
import scipy.fftpack as sf
import scipy.signal as sig 


LARGE_FONT= ("Verdana", 12)



class window(tk.Tk):
    
    def __init__(self):
        
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "ECG Project")
        
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
    
        
class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(
        self, text="Program do wyświetlania sygnałów ECG", font="Helvetica",)
        label.pack(pady=10, padx=10)

        self.pack(expand=True, fill='both')
        self.button1 = ttk.Button(self, text="wczytaj", command =lambda: self.read_in_data()).pack(pady=5,padx=10)

        self.button2 = ttk.Button(self, text="Anotacja",command =lambda: self.Annotationsave()).pack(pady=5,padx=10)
        label = tk.Label(self, text="Przycisk Wczytaj pozwala wybrać plik do wyświetlenia\nPrzycisk Anotacja pozwala zapisać anotacje", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        

    def read_in_data(self):
        ecg_path = tkinter.filedialog.askopenfilename()
        ecg_data = np.fromfile(ecg_path, dtype=int)

        fs = 360
        time = np.arange(ecg_data.size) / fs
        my_label = Label(self, text='File path: ' + ecg_path).pack()


        f = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(111)
        a.set_xlabel("czas [s]")
        a.set_ylabel("ECG in mV")
        a.set_title("Syngal EKG")
        a.set_xlim(0, 10)
        a.plot(time, ecg_data)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        
    
class Analyzer(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Analyzer", font=("Verdana", 16))
        label.pack(pady=10,padx=10)

        ttk.Button(self, text="Back to Home", command=lambda: master.switch_frame(StartPage)).pack(pady=5,padx=10)
      
        ttk.Button(self, text="Filters", command=lambda: master.switch_frame(Filters)).pack(pady=5,padx=10)
        label = tk.Label(self, text="The powerspectrum of the generated ECG signal is analyzed here!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.spectral_analysis()

    

    def spectral_analysis(self):
        # Plotting ECG
        Fs = 360
        t = 4
        f = 10

        ecg_path = tkinter.filedialog.askopenfilename()
        x = np.fromfile(ecg_path, dtype=int)
        x = (x - 1024) / 200.0
        my_label = Label(self, text='File path: ' + ecg_path).pack()

        
        n = np.arange(x.size) / Fs
        

        f = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(211)
        
        a.set_xlabel("time in s")
        a.set_ylabel("ECG in mV")
        a.set_title("ECG Signal")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.plot(n, x)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #Spectral Analysis
        x_fft = abs(sf.fft(x))
        l = np.size(x)
        fr = (Fs/2)*np.linspace(0, 1, l/2)                  
        x_magnitude = (2 / l)* abs(x_fft[0:np.size(fr)])

        f2 = Figure(figsize=(10,6), dpi=100)
        b = f.add_subplot(212)
        
        b.set_xlabel('Frequency / Hz')
        b.set_ylabel('Magnitude / dB')
        b.set_title("Spectral analysis of the ECG")
        
        b.plot(fr, 100000*x_magnitude)

        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas2, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f.tight_layout()
        f2.tight_layout()




class Filters(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Filters", font=("Verdana", 16))
        label.pack(pady=10,padx=10)

        ttk.Button(self, text="Back to Home", command=lambda: master.switch_frame(StartPage)).pack(pady=5,padx=10)
      
        ttk.Button(self, text="Analyzer", command=lambda: master.switch_frame(Analyzer)).pack(pady=5,padx=10)

        ttk.Button(self, text="High Pass Filtering", 
            command=lambda: master.switch_frame(Highpass_Filter)).pack(pady=3,padx=10)

        ttk.Button(self, text="Low Pass Filtering", 
            command=lambda: master.switch_frame(Lowpass_Filter)).pack(pady=3,padx=10)

        ttk.Button(self, text="Band Pass Filtering",
            command=lambda: master.switch_frame(Bandpass_Filter)).pack(pady=3,padx=10)

        ttk.Button(self, text="Band Stop Filtering",
            command=lambda: master.switch_frame(Bandstop_Filter)).pack(pady=3,padx=10)

        label = tk.Label(self, text="Please select your filter :)", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        

app = window()
app.mainloop()