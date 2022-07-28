import numpy as np
import time
from scipy import integrate
from scipy import optimize
import scipy as scipy
from scipy.signal import find_peaks
import matplotlib
import matplotlib.figure as figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import uniform
import datetime as dt
import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import pylab
import paho.mqtt.client as paho
import ssl
import Adafruit_ADS1x15
#from Adafruit_MAX31856 import MAX31856 as MAX31856
import logging
#import Adafruit_GPIO
#import RPi.GPIO as GPIO
from matplotlib.figure import Figure
import datetime
import pandas as pd
from tkinter.filedialog import askopenfilename




# #ADC
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1


# Parameters
update_interval = 100  # Time (ms) between polling/animation updates
max_elements = 400  # Maximum number of elements to store in plot lists
#prom_value = #standoff

name_array = []
retention_array = []
height_array = []
area_array = []



root = None
dfont = None
frame = None
canvas = None
ax1 = None
temp_plot_visible = None
dtime = []
# Global variable to remember various states
fullscreen = False
temp_plot_visible = True
light_plot_visible = True


# #Button
# GPIO.setmode(GPIO.BCM)
# pins =[22,23,17,27]
# GPIO.setwarnings(False)
# bt = 500

# #RELAY
# pinList = [16, 20, 0, 5, 6, 13, 19, 26]
# for i in pinList:
#     GPIO.setup(i, GPIO.OUT)
#     GPIO.output(i, GPIO.LOW)


# #ThermoCouple
# logging.basicConfig(
#     filename='simpletest.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# _logger = logging.getLogger(__name__)
# SPI_PORT = 0
# SPI_DEVICE = 0
# sensor = MAX31856(hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))

 
class startup:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.configure(background='black')
        self.dfont = tkFont.Font(size=-27)
        self.nfont = tkFont.Font(size=-46)
        self.textc = '#4cf55a'
        self.var=0

        for w in self.frame.winfo_children():
            w.grid(padx=5, pady=5)
            
        #parameters
        global sensor_reading
        sensor_reading = tk.DoubleVar()
        global sensor_new
        sensor_new = tk.DoubleVar()
        global temp_target
        temp_target = tk.DoubleVar()
        global calib_time
        calib_time = tk.DoubleVar()
        global sample_time
        sample_time = tk.DoubleVar()
        global inject_time
        inject_time = tk.DoubleVar()
        global analysis_time
        analysis_time = tk.DoubleVar()
        global prominence_set
        prominence_set = tk.IntVar()
        
  
        self.label_text = tk.Label(master, text="Sensor1: ", font=self.dfont, fg=self.textc,
                                   bg='black').grid(row=1,column=1)
        self.label_intro = tk.Label(master, text="Welcome to PID analzyers", font=self.dfont, fg=self.textc,
                                   bg='black').grid(row=0,column=0, columnspan=3)
        self.label_data = tk.Label(master, textvariable=sensor_reading, font=self.nfont, fg=self.textc,
                                   bg='black')
        self.button_start = tk.Button(master, text='Start', font=self.dfont, fg=self.textc, bg='black', width=8,
                                      command=lambda: self.start())
        #self.button_calib = tk.Button(master, text='Calibrate', font=self.dfont, fg=self.textc, bg='black', width=8,
        #                              command=lambda: self.calibrate())
#        self.button_tempSet = tk.Button(master, text='Set T', font=self.dfont, fg=self.textc, bg='black', width=8,
#                                      command=lambda: self.temppage())
#        self.button_method = tk.Button(master, text='Method', font=self.dfont, fg=self.textc, bg='black', width=8,
#                                      command=lambda: self.methodpage())
        
        self.label_data.grid(row=1, column=2)
        self.button_start.grid(row=3, column=0)
#        self.button_calib.grid(row=3, column=1)
#        self.button_tempSet.grid(row=3, column=2)
#        self.button_method.grid(row=3, column=3)


        master.after(150,self.GetSensor())
    
        
    def GetSensor(self):
        ## replace this with code to read sensor
        try:
            data = adc.read_adc(0, gain=GAIN)
            sensor_reading.set(data)
#           time.sleep(0.2)
        except:
            print("problem with sensor reading...")

        # Now repeat call
        self.var = self.master.after(150, self.GetSensor)

    def start(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = mainPage(self.newWindow)
        #self.newWindow.attributes("-fullscreen", True)

    def calibrate(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Calibrate(self.newWindow)
        #self.newWindow.attributes("-fullscreen", True)


    def temppage(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = tempSet(self.newWindow)
        #self.newWindow.attributes("-fullscreen", True)
        
    def methodpage(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = pMethod(self.newWindow)
        #self.newWindow.attributes("-fullscreen", True)


class Calibrate:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("600x520")
        self.frame.configure(bg='black')
        self.dfont = tkFont.Font(size=-30)
        self.nfont = tkFont.Font(size=-50)
        self.textc = '#4cf55a'
        for w in self.frame.winfo_children():
            w.grid(padx=5, pady=5)
        self.frame.pack(fill=tk.BOTH, expand=1)
        
        # #Button control
        # for i in pins:
        #     GPIO.remove_event_detect(i)
        #     time.sleep(0.1)
        #     GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #     time.sleep(0.2)
        #
        # GPIO.add_event_detect(pins[0], GPIO.FALLING, callback=lambda i: self.setdata(1),bouncetime=bt)
        # GPIO.add_event_detect(pins[1], GPIO.FALLING, callback=lambda i: self.setdata(2),bouncetime=bt)
        # GPIO.add_event_detect(pins[2], GPIO.FALLING, callback=lambda i: self.confirm,bouncetime=bt)
        # GPIO.add_event_detect(pins[3], GPIO.FALLING, callback=lambda i: self.close_windows,bouncetime=bt)


        self.calib_temp1 = tk.DoubleVar()
        self.calib_temp2 = tk.DoubleVar()
        self.calib_factor1 = tk.DoubleVar()
        self.calib_factor2 = tk.DoubleVar()
        self.calib_temp1.set(0.00)
        self.calib_temp2.set(0.00)

        self.label_name = tk.Label(self.frame, text="Value: ", font=self.dfont, fg=self.textc, bg='black').grid(row=0,
                                                                                                         column=0)
        self.label_data = tk.Label(self.frame, textvariable=sensor_reading, font=self.nfont, fg=self.textc, bg='black').grid(row=0, column=1,
                                                                                                              columnspan=5)
        self.label_calib1 = tk.Label(self.frame, textvariable=self.calib_temp1, font=self.dfont, fg=self.textc, bg='black').grid(row=1,
                                                                                                                  column=1)
        self.label_calib2 = tk.Label(self.frame, textvariable=self.calib_temp2, font=self.dfont, fg=self.textc, bg='black').grid(row=2,
                                                                                                                  column=1)
        self.label_data1 = tk.Label(self.frame, text="Factor 1", font=self.dfont, fg=self.textc, bg='black').grid(row=1, column=0)
        self.label_data2 = tk.Label(self.frame, text="Factor 2", font=self.dfont, fg=self.textc, bg='black').grid(row=2, column=0)       
        self.button_data1 = tk.Button(self.frame, text="Set 1", font=self.dfont, fg=self.textc, bg='black',width=8,
                                      command=lambda: self.setdata(1)).grid(row=3, column=0)
        self.button_data2 = tk.Button(self.frame, text="Set 2", font=self.dfont, fg=self.textc, bg='black',width=8,
                                      command=lambda: self.setdata(2)).grid(row=3, column=1)        
        self.confirmButton = tk.Button(self.frame, text='Confirm', font=self.dfont, fg=self.textc, bg='black', width=8,
                                       command=self.confirm).grid(row=3, column=2)
        self.button_quit = tk.Button(self.frame, text='Quit', font=self.dfont, fg=self.textc, bg='black', width=8,
                                    command=self.close_windows).grid(row=3, column=3)
        self.frame.pack()

    def setdata(self, i):
        if i == 1:
            self.calib_temp1.set(sensor_reading.get())
        else:
            if i == 2:
                self.calib_temp2.set(sensor_reading.get())

    def confirm(self):
        self.calib_factor1.set(self.calib_temp1)
        self.calib_factor2.set(self.calib_temp2)
        self.master.destroy()

    def close_windows(self):
        self.master.destroy()

class tempSet:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("600x520")
        self.frame.configure(bg='black')
        self.dfont = tkFont.Font(size=-30)
        self.nfont = tkFont.Font(size=-46)
        self.textc = '#4cf55a'
        for w in self.frame.winfo_children():
            w.grid(padx=5, pady=5)
        self.frame.pack(fill=tk.BOTH, expand=1)

        temp_target.set(40)
        temp_target.get()

 
        # for i in pins:
        #     GPIO.remove_event_detect(i)
        #     time.sleep(0.1)
        #     GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #     time.sleep(0.2)
        #
        # GPIO.add_event_detect(pins[0], GPIO.FALLING, callback=lambda i: self.setTemp(1),bouncetime=bt)
        # GPIO.add_event_detect(pins[1], GPIO.FALLING, callback=lambda i: self.setTemp(2),bouncetime=bt)
        # GPIO.add_event_detect(pins[2], GPIO.FALLING, callback=lambda i: self.close_winodws,bouncetime=bt)
        # GPIO.add_event_detect(pins[3], GPIO.FALLING, callback=lambda i: self.close_windows,bouncetime=bt)
        #

        self.label_time = tk.Label(self.frame, text="Target T: ", font=self.dfont, fg=self.textc,
                                   bg='black')
        self.label_set = tk.Label(self.frame, textvariable=temp_target, font=self.nfont, fg=self.textc,
                                        bg='black', )
        self.read = tk.Label(self.frame, textvariable=sensor_new, font=self.nfont, fg=self.textc,
                                        bg='black', )
        self.button_up = tk.Button(self.frame, text='++', font=self.dfont, fg=self.textc, bg='black', width=8,
                                    command=lambda: self.setTemp(1))
        self.button_down = tk.Button(self.frame, text='--', font=self.dfont, fg=self.textc, bg='black', width=8,
                                    command=lambda: self.setTemp(2))
        self.button_quit = tk.Button(self.frame, text='Quit', font=self.dfont, fg=self.textc, bg='black', width=8,
                                    command=self.close_windows)
        
        #layout
        self.label_time.grid(row=1, column=0)
        self.label_set.grid(row=1,column=1)
        self.read.grid(row=1, column=2)
        self.button_up.grid(row=2,column=0)
        self.button_down.grid(row=2,column=1)
        self.button_quit.grid(row=2,column=2)
        self.frame.pack()
        self.frame.after(150,self.GetTemp())

    def setTemp(self, i):
        if i == 1:
            temp_target.set(temp_target.get()+1)
        else:
            if i == 2:
                temp_target.set(temp_target.get()-1)

    def GetTemp(self):
        ## replace this with code to read sensor
        try:
            sensor_new.set(round(sensor.read_temp_c()))
            if sensor_new.get() > temp_target.get():
                GPIO.output(16, GPIO.LOW)
            if sensor_new.get() < temp_target.get():
                GPIO.output(16, GPIO.HIGH)
        except:
            print("problem with temperature control")

        # Now repeat call
        self.var = self.master.after(150, self.GetTemp)

    def close_windows(self):
        self.master.destroy()
        

class pMethod:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("600x520")
        self.frame.configure(bg='black')
        self.dfont = tkFont.Font(size=-30)
        self.nfont = tkFont.Font(size=-46)
        self.textc = '#4cf55a'
        for w in self.frame.winfo_children():
            w.grid(padx=5, pady=5)
        self.frame.pack(fill=tk.BOTH, expand=1)
        
                #Button control
        temp_target.set(40)
        temp_target.get()
        calib_time.set(70)
        sample_time.set(400)
        analysis_time.set(85)
        inject_time.set(22)
        self.selected = []
        style = ttk.Style()
        self.tree = ttk.Treeview(self.frame, columns = ('Name','RT'))
        self.tree.heading('#0',text='Parameters')
        self.tree.heading('#1',text='Value')
        self.tree.heading('#2',text='Status')
        self.tree.column('#0',width = 200, stretch=tk.YES)
        self.tree.column('#1',width = 200, stretch=tk.YES)
        self.tree.insert('','end',text="Calibration Time",values=(str(datetime.timedelta(seconds=calib_time.get()))))
        self.tree.insert('','end',text="Sample Time",values=(str(datetime.timedelta(seconds=sample_time.get()))))
        self.tree.insert('','end',text="Analysis Time",values=(str(datetime.timedelta(seconds=analysis_time.get()))))
        self.tree.insert('','end',text="Inject Time",values=(str(datetime.timedelta(seconds=inject_time.get()))))
        self.tree.bind('<<TreeviewSelect>>',self.on_select)
        self.time_id = 0
        child_id = self.tree.get_children()[self.time_id]
        self.tree.selection_set(child_id)


        # for i in pins:
        #     GPIO.remove_event_detect(i)
        #     time.sleep(0.1)
        #     GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #     time.sleep(0.2)
        #
        # GPIO.add_event_detect(pins[0], GPIO.FALLING, callback=lambda i: self.goUp(),bouncetime=bt)
        # GPIO.add_event_detect(pins[1], GPIO.FALLING, callback=lambda i: self.goDown(),bouncetime=bt)
        # GPIO.add_event_detect(pins[2], GPIO.FALLING, callback=lambda i: self.dialUp(),bouncetime=bt)
        # GPIO.add_event_detect(pins[3], GPIO.FALLING, callback=lambda i: self.dialDown(),bouncetime=bt)


        self.button_plus = tk.Button(self.frame, text='++', font=self.dfont, fg=self.textc, bg='black', width=10,
                                    command=lambda: self.goUp())
        self.button_minus = tk.Button(self.frame, text='--', font=self.dfont, fg=self.textc, bg='black', width=10,
                                    command=lambda: self.goDown())
        self.button_up = tk.Button(self.frame, text='up', font=self.dfont, fg=self.textc, bg='black', width=10,
                                    command=lambda: self.dialUp())
        self.button_down = tk.Button(self.frame, text='down', font=self.dfont, fg=self.textc, bg='black', width=10,
                                    command=lambda: self.dialDown())
        self.button_quit = tk.Button(self.frame, text='Quit', font=self.dfont, fg=self.textc, bg='black', width=10,
                                    command=self.close_windows)
        #layout
        self.tree.grid(row=0,column=0,columnspan=6)
        self.button_up.grid(row=1,column=0)
        self.button_down.grid(row=1,column=1)
        self.button_plus.grid(row=2,column=0)
        self.button_minus.grid(row=2,column=1)
        self.button_quit.grid(row=2,column=2)
        self.frame.pack()
        self.frame.after(150,self.GetTemp())

    def setTemp(self, i):
        if i == 1:
            temp_target.set(temp_target.get()+1)
        else:
            if i == 2:
                temp_target.set(temp_target.get()-1)
                
    def on_select(self,event):
        self.selected = event.widget.selection()
        
    def dialUp(self):
        try:
            self.time_id -= 1
            child_id = self.tree.get_children()[self.time_id]
        except:
            self.time_id =-1
            child_id = self.tree.get_children()[self.time_id]
        self.tree.selection_set(child_id)

            
    def dialDown(self):
        try:
            self.time_id += 1
            child_id = self.tree.get_children()[self.time_id]

        except:
            self.time_id = 0
            child_id = self.tree.get_children()[self.time_id]

        self.tree.selection_set(child_id)
    
    def goUp(self):
        for idx in self.selected:
            if self.tree.item(idx)['text'] == "Calibration Time":
                calib_time.set(calib_time.get()+1)
                self.time_id = 0
            elif self.tree.item(idx)['text'] == "Sample Time":
                sample_time.set(sample_time.get()+1)
                self.time_id = 1
            elif self.tree.item(idx)['text'] == "Analysis Time":
                analysis_time.set(analysis_time.get()+1)
                self.time_id = 2
            elif self.tree.item(idx)['text'] == "Inject Time":
                inject_time.set(inject_time.get()+1)
                self.time_id = 3
        self.tree.delete(*self.tree.get_children())
        self.tree.insert('','end',text="Calibration Time",values=(str(datetime.timedelta(seconds=calib_time.get()))))
        self.tree.insert('','end',text="Sample Time",values=(str(datetime.timedelta(seconds=sample_time.get()))))
        self.tree.insert('','end',text="Analysis Time",values=(str(datetime.timedelta(seconds=analysis_time.get()))))
        self.tree.insert('','end',text="Inject Time",values=(str(datetime.timedelta(seconds=inject_time.get()))))        
        child_id = self.tree.get_children()[self.time_id]
        self.tree.selection_set(child_id)
    def goDown(self):
        for idx in self.selected:
            if self.tree.item(idx)['text'] == "Calibration Time":
                calib_time.set(calib_time.get()-1)
                self.time_id = 0
            elif self.tree.item(idx)['text'] == "Sample Time":
                sample_time.set(sample_time.get()-1)
                self.time_id = 1
            elif self.tree.item(idx)['text'] == "Analysis Time":
                analysis_time.set(analysis_time.get()-1)
                self.time_id = 2
            elif self.tree.item(idx)['text'] == "Inject Time":
                inject_time.set(inject_time.get()-1)
                self.time_id = 3
        self.tree.delete(*self.tree.get_children())
        self.tree.insert('','end',text="Calibration Time",values=(str(datetime.timedelta(seconds=calib_time.get()))))
        self.tree.insert('','end',text="Sample Time",values=(str(datetime.timedelta(seconds=sample_time.get()))))
        self.tree.insert('','end',text="Analysis Time",values=(str(datetime.timedelta(seconds=analysis_time.get()))))
        self.tree.insert('','end',text="Inject Time",values=(str(datetime.timedelta(seconds=inject_time.get()))))        
        child_id = self.tree.get_children()[self.time_id]
        self.tree.selection_set(child_id)
    def GetTemp(self):
        ## replace this with code to read sensor
        try:
            sensor_new.set(round(sensor.read_temp_c()))
            if sensor_new.get() > temp_target.get():
                GPIO.output(16, GPIO.LOW)
            if sensor_new.get() < temp_target.get():
                GPIO.output(16, GPIO.HIGH)
        except:
            print("problem with temperature control")

        # Now repeat call
        self.var = self.master.after(150, self.GetTemp)

    def close_windows(self):
        self.master.destroy()
        
        
class makeplot:
    def __init__(self, master, xs, sensor, noise):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.geometry("600x520")
        master.configure(bg='black')
        self.dfont = tkFont.Font(size=-30)
        self.nfont = tkFont.Font(size=-36)
        self.textc = '#4cf55a'
        for w in self.frame.winfo_children():
            w.grid(padx=5, pady=5)
            
        #Button Control
        #self.maxdata_arr = maxdata_arr
        self.noise = noise
        fig = Figure(figsize=(6,4), dpi=100,facecolor='white')
        raw = sensor
        disp_data = [i - self.noise for i in raw]
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(xs,disp_data, color ='black')
        # Dislay the data
        peaks,properties=find_peaks(disp_data,prominence=prominence_set.get())
        #print(prominence_set.get())
        rr = properties["right_bases"]
        ll = properties["left_bases"]
        retention_array.clear()
        height_array.clear()
        area_array.clear()
        name_array.clear()

        for i in peaks:
            ax.plot(xs[i],disp_data[i],"x")
            ax.annotate('%d'% (np.where(peaks==i)),
                        xy=(xs[i]+0.1, disp_data[i]+0.1),
                        xytext=(xs[i] + 0.2, disp_data[i]+0.2),)
            
            if xs[i]<10:
                name_array.append("Benzene")
            elif xs[i]<15:
                name_array.append("C2H4")
            else:
                name_array.append("Compound-xx")
            retention_array.append(xs[i])
            height_array.append(disp_data[i])
            q = list(peaks).index(i)
            area_array.append(integrate.simps(disp_data[ll[q]:rr[q]],xs[ll[q]:rr[q]]))


        formatter = matplotlib.ticker.FuncFormatter(lambda s, x: time.strftime('%M:%S', time.gmtime(s)))
        ax.xaxis.set_major_formatter(formatter)
        ax.set_title('The reading vs. time')
        ax.set_xlabel('Time mm/ss')
        ax.set_ylabel('Reading()')
#        ax.set_ylim(-1,30)
        ax.grid(True)

#        # Peak Seperation
#        if len(self.maxdata_arr) == 2:
#            self.popt_lorentz, self.pcov_lorentz = scipy.optimize.curve_fit(self._2Lorentzian, self.xs, disp_data,
#                                                                            p0=[self.maxdata_arr[0],
#                                                                                self.maxtime_arr[0], 5,
#                                                                                self.maxdata_arr[1],
#                                                                                self.maxtime_arr[1], 5])
#
#            self.perr_lorentz = np.sqrt(np.diag(self.pcov_lorentz))
#
#            pars_1 = self.popt_lorentz[0:3]
#            pars_2 = self.popt_lorentz[3:6]
#            lorentz_peak_1 = self._1Lorentzian(self.xs, *pars_1)
#            lorentz_peak_2 = self._1Lorentzian(self.xs, *pars_2)
#
#            line, = plt.plot(self.xs, self._2Lorentzian(self.xs, *self.popt_lorentz), "k--")
#
#            # peak 1
#            plt.plot(self.xs, lorentz_peak_1, "g")
#            plt.fill_between(self.xs, lorentz_peak_1.min(), lorentz_peak_1, facecolor="green", alpha=0.5)
#
#            # peak 2
#            plt.plot(self.xs, lorentz_peak_2, "y")
#            plt.fill_between(self.xs, lorentz_peak_2.min(), lorentz_peak_2, facecolor="yellow", alpha=0.5)
#
#            i_simp_1 = integrate.simps(lorentz_peak_1, self.xs)
#            i_simp_2 = integrate.simps(lorentz_peak_2, self.xs)
#
#            isimp = []
#            isimp.append(i_simp_1)
#            isimp.append(i_simp_2)
#            # annotation
#            for i in range(len(self.maxdata_arr)):
#                ax.annotate('The Max is %d. \n The retention time is %d s. \n The area is %d.'
#                            % (self.maxdata_arr[i], self.maxtime_arr[i], isimp[i]),
#                            xy=(self.maxtime_arr[i] + 0.5, self.maxdata_arr[i] / 1.5),
#                            xytext=(self.maxtime_arr[i] + 2.5, self.maxdata_arr[i] / 1.5 + 5),
#                            arrowprops=dict(facecolor='black', shrink=0.05), )
        
        canvas = FigureCanvasTkAgg(fig, master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,columnspan = 4)
        self.button_report = tk.Button(master, text='Report', font=self.dfont, fg=self.textc, bg='black', width=8,
                                       command=lambda: self.report())
        self.button_import = tk.Button(master, text='Import',font=self.dfont, fg=self.textc, bg='black', width=8,
                                       command=lambda: self.import_data())
        self.button_save_plot = tk.Button(master, text='Save Plot',font=self.dfont, fg=self.textc, bg='black', width=8,
                                       command=lambda: self.save_plot(sensor,xs))
        self.button_quit= tk.Button(master, text='Quit', font=self.dfont, fg=self.textc, bg='black', width=8,
                                      command=self.close_windows)

        self.button_report.grid(row=1,column=0)
        self.button_import.grid(row=1,column=1)
        self.button_save_plot.grid(row=1,column=2)
        self.button_quit.grid(row=1, column=3)

        # for i in pins:
        #     GPIO.remove_event_detect(i)
        #     time.sleep(0.1)
        #     GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #     time.sleep(0.2)
        #
        # GPIO.add_event_detect(pins[0], GPIO.FALLING, callback=lambda i: self.report,bouncetime=bt)
        # GPIO.add_event_detect(pins[3], GPIO.FALLING, callback=lambda i: self.close_windows,bouncetime=bt)

        
    def report(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = report(self.newWindow)
        #self.newWindow.attributes("-fullscreen",True)

    def save_plot(self,sensor,xs):
        
        fig, (ax1, ax2) = plt.subplots(2,1)
        raw = sensor
        disp_data = [i - self.noise for i in raw]
        ax1.plot(xs, disp_data, color='black')
        # Dislay the data
        peaks, properties = find_peaks(disp_data, prominence=prominence_set.get())
        rr = properties["right_bases"]
        ll = properties["left_bases"]
        for i in peaks:
            ax1.plot(xs[i], disp_data[i], "x")
            ax1.annotate('%d' % (np.where(peaks == i)),
                        xy=(xs[i] + 0.1, disp_data[i] + 0.1),
                        xytext=(xs[i] + 0.2, disp_data[i] + 0.2), )


        formatter = matplotlib.ticker.FuncFormatter(lambda s, x: time.strftime('%M:%S', time.gmtime(s)))
        ax1.xaxis.set_major_formatter(formatter)
        ax1.set_title('GC Report 03/23',fontsize=20)
        ax1.set_xlabel('Time mm/ss')
        ax1.set_ylabel('Reading()')
        #        ax.set_ylim(-1,30)
        ax1.grid(True)
        cell = []
        row = []
        column = ["Compound","Concentration","Retention Time", "Area"]
        colors = plt.cm.BuPu(np.linspace(0, 0.5, len(retention_array)))
        colors = colors[::-1]
        try:
            for i in range(len(retention_array)):
                cell.append([name_array[i],
                             "{:10.2f}".format(height_array[i]/1000000) + " ppb",
                             "{:10.2f}".format(retention_array[i]) + " s",
                             "{:10.2f}".format(area_array[i])])
                row.append(i)
        except:
            pass

        ax2.axis('tight')
        ax2.axis('off')
        the_table = ax2.table(cellText=cell,
                              rowLabels=row,
                              rowColours=colors,
                              colLabels=column,
                              loc='center')
        cell2 = [["Model Name", "model 102"],
                 ["Serial #","xxxx-xxxx"],
                 ["GPS location",92],
                 ["Date","03/23/2020"],
                 ["Prominence", 30000]]
        the_table2 = ax2.table(cellText=cell2,
                               loc='bottom')
        plt.tight_layout()
        plt.savefig('GC Report.png')
        print("Plot saved")

    def import_data(self):

        filepath = askopenfilename()
        df = pd.read_csv(filepath, nrows=900)
        self.newWindow = tk.Toplevel(self.master)
        self.xs = df['Time'].tolist()
        self.sensor1_array = df["Sensor1"].tolist()
        self.noise = 10
        self.app = makeplot(self.newWindow,self.xs, self.sensor1_array, self.noise)
        #self.newWindow.attributes("-fullscreen",True)
    
    def _1gaussian(self, x, amp1, cen1, sigma1):
        return amp1 * (1 / (sigma1 * (np.sqrt(2 * np.pi)))) * (np.exp((-1.0 / 2.0) * (((T - cen1) / sigma1) ** 2)))

    def _2gaussian(self, x, amp1, cen1, sigma1, amp2, cen2, sigma2):
        return amp1 * (1 / (sigma1 * (np.sqrt(2 * np.pi)))) * (np.exp((-1.0 / 2.0) * (((T - cen1) / sigma1) ** 2))) + \
               amp2 * (1 / (sigma2 * (np.sqrt(2 * np.pi)))) * (np.exp((-1.0 / 2.0) * (((T - cen2) / sigma2) ** 2)))

    def _1Lorentzian(self, x, amp, cen, wid):
        return amp * wid ** 2 / ((x - cen) ** 2 + wid ** 2)

    def _2Lorentzian(self, x, amp1, cen1, wid1, amp2, cen2, wid2):
        return (amp1 * wid1 ** 2 / ((x - cen1) ** 2 + wid1 ** 2)) + \
               (amp2 * wid2 ** 2 / ((x - cen2) ** 2 + wid2 ** 2))
    
    def close_windows(self):
        self.master.destroy()


class report:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.configure(background='black')
        self.dfont = tkFont.Font(size=-30)
        self.nfont = tkFont.Font(size=-36)
        self.textc = '#4cf55a'
        for w in self.frame.winfo_children():
            w.grid(padx=5, pady=5)
        self.tree = ttk.Treeview(master, columns = ('Name','RT','Height','Area'))
        self.tree.heading('#0',text='Number')
        self.tree.heading('#1',text='Name')
        self.tree.heading('#2',text='RT')
        self.tree.heading('#3',text='Height')
        self.tree.heading('#4',text='Area')
        self.tree.column('#0',width = 130, stretch=tk.YES)
        self.tree.column('#1',width = 130, stretch=tk.YES)
        self.tree.column('#2',width = 130, stretch=tk.YES)
        self.tree.column('#3',width = 130, stretch=tk.YES)
        self.tree.column('#4',width = 130, stretch=tk.YES)
        #self.peak = tk.Text(master, height=15, width=60, font=tkFont.Font(size=-15), fg=self.textc, bg='black')
        self.button_quit= tk.Button(master, text='Quit', font=self.dfont, fg=self.textc, bg='black', width=20,
                                      command=self.close_windows)
        
        #layout
        #self.peak.grid(row=0,column=0)
        self.tree.grid(row=0,columnspan=1,sticky='nsew')
        self.button_quit.grid(row=1, column=0) 
        #self.peak.insert(tk.END, " #   Name   R-Time Height  Area\n")


        # for i in pins:
        #     GPIO.remove_event_detect(i)
        #     time.sleep(0.1)
        #     GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #     time.sleep(0.2)
        #
        # GPIO.add_event_detect(pins[0], GPIO.FALLING, callback=lambda i: self.close_windows,bouncetime=bt)
        # GPIO.add_event_detect(pins[1], GPIO.FALLING, callback=lambda i: self.close_windows,bouncetime=bt)
        # GPIO.add_event_detect(pins[2], GPIO.FALLING, callback=lambda i: self.close_windows,bouncetime=bt)
        # GPIO.add_event_detect(pins[3], GPIO.FALLING, callback=lambda i: self.close_windows,bouncetime=bt)

        for i in range(len(retention_array)):
            self.tree.insert('','end',text=str(i),values=(name_array[i],
                                                          "{:10.2f}".format(retention_array[i]) + " s",
                                                          "{:10.2f}".format(height_array[i]),
                                                          "{:10.2f}".format(area_array[i])))
            #self.peak.insert(tk.END, "%d : %s  %.2fs  %.2f %.2f \n"
            #                  %(i, name_array[i],retention_array[i], height_array[i], area_array[i]))

        #print(len(retention_array))

               
    def close_windows(self):
        self.master.destroy()
        
class mainPage:
    def __init__(self, master):
        xs = []
        sensor1_array = []
        self.sensor_array = []
        self.maxdata_arr = []
        self.maxtime_arr = []
        self.max_temp_c = tk.DoubleVar()
        self.onoff = tk.StringVar()
        self.onoff.set("Pause")
        self.sensor1_array = sensor1_array
        self.xs = xs
        self.sum = 0
        self.fall_count = 0
        self.max_temp = 0
        self.rise_count = 0
        self.max_time = 0
        self.noise = 0
        self.buttonwidth = 10
        self.state = tk.BooleanVar()
        self.state.set(False)
        self.dfont = tkFont.Font(size=-30)
        self.nfont = tkFont.Font(size=-46)
        self.textc = '#4cf55a'
        self.master = master
        self.buttonwidth = 7
        self.frame = tk.Frame(self.master)
        self.frame.configure(background='black')
        self.start = time.monotonic()
        for w in self.frame.winfo_children():
            w.grid(padx=2, pady=2)
            
        # Layout
        self.choices = {'Reading', 'Sensor2', 'Sensor3', 'Sensor4', 'Sensor5'}
        self.choice = tk.StringVar()
        self.choice.set('Reading')
        self.label_disp = tk.Label(self.frame, textvariable=self.choice, font=self.dfont, fg=self.textc,
                                   bg='black').grid(row=0, column=1)
        self.label_temp = tk.Label(self.frame, textvariable=sensor_reading, font=self.nfont, fg=self.textc, bg='black', ).grid(
            row=0, column=2)
        self.peak = tk.Text(self.frame, height=3, width=30, font=tkFont.Font(size=-20), fg=self.textc, bg='black')
        self.peak.grid(row=6, column=0, columnspan=4)
        # self.slider = tk.Scale(master, from_=10000, to=50000, orient=tk.HORIZONTAL,length=250,bg='black',fg='#4cf55a',troughcolor='#003300').grid(row=7,column=0)
        # self.slider.set(30000)
        prominence_set.set(30000)
        self.button_pause = tk.Button(self.frame, textvariable=self.onoff, font=self.dfont, fg=self.textc, bg='black', width=self.buttonwidth,
                                      command=lambda: self.dpause()).grid(row=7, column=0)
        self.button_makeplot = tk.Button(self.frame, text='Analysis', font=self.dfont, fg=self.textc, bg='black',
                                         width=10,
                                         command=lambda: self.make_plot()).grid(row=7, column=2)
        self.button_save = tk.Button(self.frame, text='Save', font=self.dfont, fg=self.textc, bg='black', width=self.buttonwidth,
                                     command=lambda: self.dsave()).grid(row=7, column=1)
#        self.button_onoff = tk.Button(self.frame, text='Valve1', font=self.dfont, fg=self.textc, bg='black', width=self.buttonwidth,
 #                                     command=lambda: self.g_button(0)).grid(row=7, column=0)
        self.button_close = tk.Button(self.frame, text='Quit', font=self.dfont, fg=self.textc, bg='black', width=self.buttonwidth,
                                      command=lambda: self.close_windows()).grid(row=7, column=3)

        self.frame.pack(fill=tk.BOTH, expand=1)
        # make figure animation
        self.fig = figure.Figure(figsize=(6.7, 3),facecolor="black")
        self.fig.subplots_adjust(left=0.1, right=0.9)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_plot = self.canvas.get_tk_widget()
        self.canvas_plot.grid(row=2, column=0, rowspan=3, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)
        self.fargs = (ax1, xs, sensor1_array, sensor_reading)
        self.ani = animation.FuncAnimation(self.fig, self.animate, fargs=self.fargs, interval=update_interval)


        # for i in pins:
        #     GPIO.remove_event_detect(i)
        #     time.sleep(0.1)
        #     GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #     time.sleep(0.2)
        #
        # GPIO.add_event_detect(pins[0], GPIO.FALLING, callback=lambda i: self.dpause(),bouncetime=bt)
        # GPIO.add_event_detect(pins[1], GPIO.FALLING, callback=lambda i: self.dsave(),bouncetime=bt)
        # GPIO.add_event_detect(pins[2], GPIO.FALLING, callback=lambda i: self.make_plot(),bouncetime=bt)
        # GPIO.add_event_detect(pins[3], GPIO.FALLING, callback=lambda i: self.close_windows(),bouncetime=bt)
        #
    def g_button(self, pin):
        print(GPIO.input(pin))
        if GPIO.input(pin) == 1:
            GPIO.output(pin, GPIO.LOW)
        elif GPIO.input(pin) == 0:
            GPIO.output(pin, GPIO.HIGH)

    def dpause(self):
        if self.onoff.get() == "Pause":
            self.ani.event_source.stop()
            self.onoff.set("Resume")
        elif self.onoff.get() == "Resume":
            self.ani.event_source.start()
            self.onoff.set("Pause")

    def close_windows(self):
        self.master.destroy()

    def upload(self):
        from subprocess import Popen
        Popen(["python", "aws_publish.py"])
        pass

    def dsave(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.file = open(timestr, "a")
        if os.stat(timestr).st_size == 0:
            self.file.write("Time,Sensor1\n")
        i = 0
        while i < len(self.sensor1_array):
            self.file.write(str("{0:.2g}".format(self.xs[i])) + ","
                            + str(self.sensor1_array[i]) + "\n")
            i = i + 1
            self.file.flush()
        self.peak.insert(tk.END, "Saved to "+timestr+"\n")

    def make_plot(self):
        time.sleep(3)
        self.newWindow = tk.Toplevel(self.master)
        self.app = makeplot(self.newWindow,self.xs, self.sensor1_array, self.noise)
        #self.newWindow.attributes("-fullscreen",True)
    def animate(self, i, ax1, xs, data_read, temp_c):

        try:
            new_reading = sensor_reading.get()

            # new_data = round(uniform(20.0, 25.0), 2)
        except:
            print("not getting sensor value")
            
        #moving average
        if len(self.sensor_array) < 5:
            self.sensor_array.append(new_reading)
        else:
            self.sensor_array.pop(0)
            self.sensor_array.append(new_reading)
        new_data = np.mean(self.sensor_array)
        temp_c.set('%.1f' % new_data)
        
        now = time.monotonic() - self.start
        xs.append(now)            
        data_read.append(new_data)
        
        if now > 300:
            self.ani.event_source.stop()
            self.newWindow = tk.Toplevel(self.master)
            self.app = makeplot(self.newWindow,self.xs, self.sensor1_array, self.noise)
            
        
        #limit the size of the readings
        xs = xs[-max_elements:]
        data_read = data_read[-max_elements:]
        
        #zero out the noises
        if len(data_read) == 1:
            self.peak.insert(tk.END, "Wait for calibration... \n")

        if len(data_read) == 30:
            self.noise = np.mean(data_read)
            self.peak.insert(tk.END, "Noise is %d. Ready to measure.\n" % (self.noise))
        
        #peak finding
        if new_data > 20:
            if new_data > self.max_temp:
                self.max_temp = new_data
                self.fall_count -= 1
                self.max_time = now
                self.rise_count += 1
            elif new_data < self.max_temp and self.fall_count > 10:
                self.max_temp = 0
                self.fall_count = 0
            elif self.fall_count > 7 and self.rise_count > 5:
                self.fall_count = 0
                self.rise_count = 0
                self.maxdata_arr.append(self.max_temp)
                self.maxtime_arr.append(self.max_time)
                self.peak.insert(tk.END, "Found max at %d @ %d s.\n" % (self.max_temp, self.max_time))
                self.max_temp = 0
            elif temp_c.get() < self.max_temp:
                self.fall_count += 1
                if self.rise_count > 0 and self.rise_count < 6:
                    self.rise_count -= 1
        self.ax1.clear()
        self.ax1.grid()
        self.ax1.set_ylabel('Sensor1 Data', color='#4cf55a',fontsize=16)
        self.ax1.tick_params(axis='y', labelcolor='#4cf55a')
        self.ax1.set_facecolor('black')
        if max(data_read) <30:
            self.ax1.set_ylim(-5,30)
        self.ax1.fill_between(xs, data_read, 0, linewidth=2, color='green', alpha=0.5)
        formatter = matplotlib.ticker.FuncFormatter(lambda s, x: time.strftime('%M:%S', time.gmtime(s)))
        self.ax1.xaxis.set_major_formatter(formatter)
        self.ax1.tick_params(axis='x', labelcolor='#4cf55a')
        self.ax1.collections[0].set_visible(temp_plot_visible)
        
        # AWS
        ts =  time.time()

        # Temperature control
        # pid = PID(1, 0.1, 0.05, setpoint = desired_value)
        # Pi_output = pid(Pi_input)
        time.sleep(0.2)


def toggle_fullscreen(root):
    root.attributes('-fullscreen',True)
def end_fullscreen(root):
    root.attributes('-fullscreen',False)

def main():
    root = tk.Tk()
    app = startup(root)
    root.title("Welcome to PID Analyzer")
    root.configure(background="black")
    root.attributes('-fullscreen', False)
    root.geometry('700x520')
    root.bind('<Return>',lambda event:toggle_fullscreen(root))
    root.bind('<Escape>',lambda event:end_fullscreen(root))
    root.mainloop()
    

if __name__ == '__main__':
    main()

