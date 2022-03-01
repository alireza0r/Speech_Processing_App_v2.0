# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 19:52:49 2021

@author: Alireza Rahmati (AR)
"""

# ********************
import subfunction
import processing
# ********************
import tkinter as tk
from tkinter import ttk
#from tkinter import filedialog as fd
import tkinter.messagebox
from PIL import Image, ImageTk
# ********************
import os
# ********************
import scipy.signal.windows as ssw
# ********************

ICON_DIR = os.getcwd() + '/sys_file/icon/'

function = subfunction.Function('sys_file/system_file.wav')
sub_function = function.SubFunction
properties_function = function.Properties
fun_signal_process = function.ProseccingSubFun

class Gui:
    def __init__(self, root_window):
        self.root_window = root_window
        
        print('Gui configed')
        
    def RunGui(self):
        self.root_window.title('AR_Voice')
        self.root_window.geometry("280x90")
        
        #img = tk.PhotoImage(ICON_DIR + 'icon.png')
        self.root_window.iconbitmap(ICON_DIR + 'icon.ico')
        
        # Create menu bar
        menu_bar = tk.Menu(self.root_window, tearoff=0)
    
        # sub menu bar - file
        sub_menu_bar = tk.Menu(menu_bar)
        sub_menu_bar.add_command(label='Open', command=lambda sub_fun_name='open_file': sub_function(sub_fun_name))
        sub_menu_bar.add_command(label='Save', command=lambda sub_fun_name='save_file': sub_function(sub_fun_name))
        sub_menu_bar.add_command(label='Save as...', command=lambda sub_fun_name='save_file_as': sub_function(sub_fun_name))
        sub_menu_bar.add_separator()
        sub_menu_bar.add_command(label='Exit', command=self.root_window.destroy)
        menu_bar.add_cascade(label='File', menu=sub_menu_bar)
    
        # sub menu bar - edit
        sub_menu_bar = tk.Menu(menu_bar)
        sub_menu_bar.add_command(label="Play", command=lambda sub_fun_name='play_file': sub_function(sub_fun_name))
        sub_menu_bar.add_command(label="Pause", command=lambda sub_fun_name='pause_file': sub_function(sub_fun_name))
        sub_menu_bar.add_command(label="Resume", command=lambda sub_fun_name='resume_file': sub_function(sub_fun_name))
        sub_menu_bar.add_command(label="Stop", command=lambda sub_fun_name='stop_file': sub_function(sub_fun_name))
        sub_menu_bar.add_separator()
        sub_menu_bar.add_command(label="Record", command=lambda sub_fun_name='start_record': sub_function(sub_fun_name))
        sub_menu_bar.add_command(label="Pause", command=lambda sub_fun_name='pause_record': sub_function(sub_fun_name))
        sub_menu_bar.add_command(label="Resume", command=lambda sub_fun_name='resume_record': sub_function(sub_fun_name))
        sub_menu_bar.add_command(label="Stop", command=lambda sub_fun_name='stop_record': sub_function(sub_fun_name))
        sub_menu_bar.add_separator()
        sub_menu_bar.add_command(label="Properties", command=self.Properties)
        menu_bar.add_cascade(label='Edit', menu=sub_menu_bar)
        
        # sub menu bar - process
        sub_menu_bar = tk.Menu(menu_bar)
        sub_menu_bar.add_command(label="Draw", command=self.ProcessWin)
        #sub_menu_bar.add_command(label="Draw MFCC", command=lambda sub_process_name='process_mfcc': sun_signal_process(sub_process_name))
        menu_bar.add_cascade(label='Process', menu=sub_menu_bar)
    
        # sub menu bar - about
        sub_menu_bar = tk.Menu(menu_bar)
        sub_menu_bar.add_command(label="About", command=lambda sub_fun_name='about': sub_function(sub_fun_name))
        menu_bar.add_cascade(label='Help', menu=sub_menu_bar)
        
        self.root_window.config(menu=menu_bar)
        
        # Button - player
        # Create a photoimage object of the image in the path
        # play
        img = Image.open(ICON_DIR + 'play.png')
        img_created = ImageTk.PhotoImage(img)

        button = tk.Button(self.root_window, command=lambda sub_fun_name='play_file': sub_function(sub_fun_name), image=img_created)
        button.image = img_created
        button.grid(row=1, column=0)
        
        # Button - player
        # Create a photoimage object of the image in the path
        # puase
        img = Image.open(ICON_DIR + 'pause.png')
        img_created = ImageTk.PhotoImage(img)

        button = tk.Button(self.root_window, command=lambda sub_fun_name='pause_file': sub_function(sub_fun_name), image=img_created)
        button.image = img_created
        button.grid(row=1, column=5)
        
        # Button - player
        # Create a photoimage object of the image in the path
        # resume
        img = Image.open(ICON_DIR + 'resume.png')
        img_created = ImageTk.PhotoImage(img)

        button = tk.Button(self.root_window, command=lambda sub_fun_name='resume_file': sub_function(sub_fun_name), image=img_created)
        button.image = img_created
        button.grid(row=1, column=10)
        
        # Button - player
        # Create a photoimage object of the image in the path
        # Stop
        img = Image.open(ICON_DIR + 'stop.png')
        img_created = ImageTk.PhotoImage(img)

        button = tk.Button(self.root_window, command=lambda sub_fun_name='stop_file': sub_function(sub_fun_name), image=img_created)
        button.image = img_created
        button.grid(row=1, column=15)
        
        # Button - Recorder
        # Create a photoimage object of the image in the path
        # Stop
        img = Image.open(ICON_DIR + 'record.png')
        img_created = ImageTk.PhotoImage(img)

        button = tk.Button(self.root_window, command=lambda sub_fun_name='start_record': sub_function(sub_fun_name), image=img_created)
        button.image = img_created
        button.grid(row=6, column=0)
        
        # Button - Recorder
        # Create a photoimage object of the image in the path
        # Stop
        img = Image.open(ICON_DIR + 'pause.png')
        img_created = ImageTk.PhotoImage(img)

        button = tk.Button(self.root_window, command=lambda sub_fun_name='pause_record': sub_function(sub_fun_name), image=img_created)
        button.image = img_created
        button.grid(row=6, column=5)
        
        # Button - Recorder
        # Create a photoimage object of the image in the path
        # Stop
        img = Image.open(ICON_DIR + 'resume.png')
        img_created = ImageTk.PhotoImage(img)

        button = tk.Button(self.root_window, command=lambda sub_fun_name='resume_record': sub_function(sub_fun_name), image=img_created)
        button.image = img_created
        button.grid(row=6, column=10)
        
        # Button - Recorder
        # Create a photoimage object of the image in the path
        # Stop
        img = Image.open(ICON_DIR + 'stop_rec.png')
        img_created = ImageTk.PhotoImage(img)

        button = tk.Button(self.root_window, command=lambda sub_fun_name='stop_record': sub_function(sub_fun_name), image=img_created)
        button.image = img_created
        button.grid(row=6, column=15)
        
        function.ShowStatusInit(self.root_window, 1, 50, status_text='Empty')        
        function.MainWinName(self.root_window)
        
        return 1
    
    def Properties(self):
        self.var_format = tk.StringVar()
        self.var_channels = tk.StringVar()
        var_rate = tk.StringVar()
    
        select_format = ('8bit', '16bit', '32bit')
        select_channels = ('mono', 'sterio')
        
        new_win = tk.Toplevel(self.root_window)
        new_win.title('Properties')
        new_win.iconbitmap(ICON_DIR + 'icon.ico')
        #new_win.minsize(100,150)
        #new_win.maxsize(300,300)
        #new_win.geometry("500x500")
        
        # return {'audio_format':format, 'channels':channels, 'rate':rate}
        audio_result = function.ReturnAudioInit()
        format_init = audio_result['audio_format']
        channels_init = int(audio_result['channels'])
        rate_init = int(audio_result['rate'])
        
        if format_init == 16:
            format_init = '8bit'
        elif format_init == 8:
            format_init = '16bit'
        elif format_init == 2:
            format_init = '32bit'
        else:
            print('error for format_init')
        
        
        tk.Label(new_win, text='format').grid(row=1, column=0)
        com_format = ttk.Combobox(new_win, textvariable=self.var_format, width=10)
        com_format['values'] = select_format
        com_format['state'] = 'readonly'
        com_format.set(format_init) #.set(select_format[1])
        com_format.grid(row=1, column=1)
        
        tk.Label(new_win, text='Channels').grid(row=2, column=0)
        com_channels = ttk.Combobox(new_win, textvariable=self.var_channels, width=10)
        com_channels['values'] = select_channels
        com_channels['state'] = 'readonly'
        com_channels.current(channels_init - 1) #select_channels[0])
        com_channels.grid(row=2, column=1)
        
        tk.Label(new_win, text='Rate').grid(row=3, column=0)
        ent_rate = tk.Entry(new_win, textvariable=var_rate, width=10)
        ent_rate.insert(0, rate_init)
        ent_rate.grid(row=3, column=1)
        
        button = tk.Button(new_win, text='OK', command=lambda :properties_function(new_win, com_format, com_channels, ent_rate))
        button.grid(row=5, column=3)
        button = tk.Button(new_win, text='Cancel', command=new_win.destroy)
        button.grid(row=5, column=2)
    
    def ProcessWin(self):
        print('ProcessWin')
        
        self.wave = tk.IntVar()
        self.mfcc = tk.IntVar()
        self.spec = tk.IntVar()
        
        offset = tk.StringVar()
        duration = tk.StringVar()
        
        fun_signal_process('process_load')
        sig_info = fun_signal_process('process_info')
        print(sig_info)
        
        process_list_win = tk.Toplevel(self.root_window) 
        process_list_win.title('Segmantation')
        process_list_win.iconbitmap(ICON_DIR + 'icon.ico')
        
        # deactive close [X] icon
        def disable_event():
            #pass
            self.DrawClose(process_list_win)
            
        process_list_win.protocol("WM_DELETE_WINDOW", disable_event)
        # hidden Root window
        self.root_window.withdraw()
        
        tk.Label(process_list_win, text='Signal len.(Second): ').grid(row=0, column=1)
        tk.Label(process_list_win, text=sig_info[0]).grid(row=0, column=2)
        tk.Label(process_list_win, text='Signal len.(sample): ').grid(row=1, column=1)
        tk.Label(process_list_win, text=sig_info[1]).grid(row=1, column=2)
        
        tk.Label(process_list_win, text='Offset (Second): ').grid(row=0, column=3)
        I = tk.Entry(process_list_win, textvariable=offset, width=6)
        I.insert(0, '0.0')
        I.grid(row=0, column=4)
        tk.Label(process_list_win, text='Duration (Second): ').grid(row=1, column=3)
        I = tk.Entry(process_list_win, textvariable=duration, width=6)
        I.insert(0, str(sig_info[0]))
        I.grid(row=1, column=4)
        
        signal_time_details = [offset, duration]
        button = tk.Button(process_list_win, text='CreateNewPlot', command=lambda signal_time_details=signal_time_details, win_name=process_list_win: self.DrawWin(signal_time_details, win_name))
        button.grid(row=8, column=20)
        button = tk.Button(process_list_win, text='Frame', command=lambda signal_time_details=signal_time_details, win_name=process_list_win: self.FrameWin(signal_time_details, win_name))
        button.grid(row=8, column=10)
        button = tk.Button(process_list_win, text='Close', command=lambda win_name=process_list_win: self.DrawClose(win_name))
        button.grid(row=8, column=8)
        
    def DrawWin(self, signal_time_details, win_name):
        print('DrawWin')
        
        wave = tk.IntVar()
        mfcc = tk.IntVar()
        spec = tk.IntVar()
        fft = tk.IntVar()
        pre_emphasis_coef = tk.IntVar()
        pre_emphasis_frame = tk.IntVar()
        auto_pre_emphasis_sig = tk.IntVar()
        wave_frame = tk.IntVar()
        
        win_len = tk.StringVar()
        hop = tk.StringVar()
        n_fft = tk.StringVar()
        n_mfcc = tk.StringVar()
        sig_window = tk.StringVar()
        frame_win_num = tk.StringVar()
        alpha = tk.StringVar()
        pre_emphasis_sig_var = tk.StringVar()
        
        #draw_win = tk.Toplevel(self.process_list_win)
        draw_win = tk.Toplevel(win_name)
        draw_win.title('Process')
        draw_win.iconbitmap(ICON_DIR + 'icon.ico')
        #draw_win.geometry('200x800')
            
        draw_win_frame = tk.Frame(draw_win, highlightbackground="black", highlightthickness=2)#,width=200, height=200)
        draw_win_frame.grid(row=1, column=0)
        
        # Signal details
        tk.Label(draw_win_frame, text='#Config').grid(row=0, column=0)
        
        tk.Label(draw_win_frame, text='Win. length (n): ').grid(row=1, column=0)
        I = tk.Entry(draw_win_frame, textvariable=win_len, width=6)
        I.insert(0, '512')
        I.grid(row=1, column=1)
        tk.Label(draw_win_frame, text='Hop (M): ').grid(row=2, column=0)
        I = tk.Entry(draw_win_frame, textvariable=hop, width=6)
        I.insert(0, '256')
        I.grid(row=2, column=1)
    
        # Pre-emphasis signal
        ttk.Radiobutton(draw_win_frame, text='Without Pre-Emph.', variable=pre_emphasis_sig_var, value='without_emphasis').grid(row=3, column=0)
        ttk.Radiobutton(draw_win_frame, text='Auto Pre-Emph.', variable=pre_emphasis_sig_var, value='auto_emphasis').grid(row=4, column=0)
        ttk.Radiobutton(draw_win_frame, text='Manual Pre-Emph.', variable=pre_emphasis_sig_var, value='manual_emphasis').grid(row=5, column=0)
        pre_emphasis_sig_var.set('without_emphasis')
        tk.Label(draw_win_frame, text='Alpha: ').grid(row=5, column=1)
        I = tk.Entry(draw_win_frame, textvariable=alpha, width=6)
        I.insert(0, '0.9')
        I.grid(row=5, column=2)
        
        # signal Window
        window_dict = {'Rectangular':ssw.boxcar, 'Hann':ssw.hann, 'Hamming':ssw.hamming}
        tk.Label(draw_win_frame, text='Windowing: ').grid(row=8, column=0)
        com_window = ttk.Combobox(draw_win_frame, textvariable=sig_window, width=10)
        com_window['values'] = list(window_dict.keys())
        com_window['state'] = 'readonly'
        com_window.current(1) # initial to hann
        com_window.grid(row=8, column=1)
        
        # FFT
        tk.Label(draw_win_frame, text='FFT (n): ').grid(row=9, column=0)
        I = tk.Entry(draw_win_frame, textvariable=n_fft, width=6)
        I.insert(0, '2048')
        I.grid(row=9, column=1)
        
        # Show signal
        tk.Label(draw_win_frame, text='#Show Sig.').grid(row=10, column=0)
            
        # wave
        C = tk.Checkbutton(draw_win_frame, text = "Wave", variable = wave, onvalue = 1, offvalue = 0)
        C.grid(row=11, column=0)
        
        # MFCC
        C = tk.Checkbutton(draw_win_frame, text = "MFCC", variable = mfcc, onvalue = 1, offvalue = 0)
        C.grid(row=12, column=0)
        tk.Label(draw_win_frame, text='MFCC (n): ').grid(row=12, column=1)
        I = tk.Entry(draw_win_frame, textvariable=n_mfcc, width=6)
        I.insert(0, '40')
        I.grid(row=12, column=2)
        
        # Spectrogram
        C = tk.Checkbutton(draw_win_frame, text = "Spec.", variable = spec, onvalue = 1, offvalue = 0)
        C.grid(row=13, column=0)
        
        # pre-emphasis coafficiant
        C = tk.Checkbutton(draw_win_frame, text = "pre-emphasis", variable = pre_emphasis_coef, onvalue = 1, offvalue = 0)
        C.grid(row=14, column=0)
        
        # a Framed signal
        tk.Label(draw_win_frame, text='#a frame').grid(row=17, column=0)
        
        # frame number
        tk.Label(draw_win_frame, text='Frame Num.: ').grid(row=18, column=0)
        I = tk.Entry(draw_win_frame, textvariable=frame_win_num, width=6)
        I.insert(0, '0')
        I.grid(row=18, column=1)
        
        # wave on frame
        C = tk.Checkbutton(draw_win_frame, text = "Wave", variable = wave_frame, onvalue = 1, offvalue = 0)
        C.grid(row=19, column=0)
        
        # a frame FFT
        C = tk.Checkbutton(draw_win_frame, text = "FFT ", variable = fft, onvalue = 1, offvalue = 0)
        C.grid(row=20, column=0)
        
        # frame Pre-emphassis
        C = tk.Checkbutton(draw_win_frame, text = "Auto Pre-Emph. frame", variable = pre_emphasis_frame, onvalue = 1, offvalue = 0)
        C.grid(row=21, column=0)
        
        # Close and Apply  
        offset = signal_time_details[0].get()
        duration = signal_time_details[1].get()      
        sig_name_dict = {'wave':wave, 'mfcc':mfcc, 'spec':spec, 'fft':fft, 'pre_emphasis_coef':pre_emphasis_coef, 'pre_emphasis_frame':pre_emphasis_frame, 'wave_frame':wave_frame}
        sig_details_dict = {'win_len':win_len, 'hop':hop, 'n_fft':n_fft, 'n_mfcc':n_mfcc, 'window':[window_dict, sig_window], 'frame_win_num':frame_win_num, 'pre_emphasis_sig':[pre_emphasis_sig_var, alpha], 'auto_pre_emphasis_sig':auto_pre_emphasis_sig,
                            'signal_time_details':[offset, duration]}
        button = tk.Button(draw_win_frame, text='Apply', command=lambda window=draw_win, sig_details_dict=sig_details_dict: self.DrawWinVar(window, sig_name_dict, sig_details_dict))
        button.grid(row=24, column=2)
        button = tk.Button(draw_win_frame, text='Close', command=draw_win.destroy)
        button.grid(row=24, column=1)
        
    def FrameWin(self, signal_time_details, win_name):
        print('ShowSigDetails')
        
        win_len = tk.StringVar()
        hop = tk.StringVar()
        sig_window = tk.StringVar()
        frame_win_num_of = tk.StringVar()
        frame_win_num_to = tk.StringVar()
        alpha = tk.StringVar()
        pre_emphasis_frame_var = tk.StringVar()
        n_fft = tk.StringVar()
        p_lpc = tk.StringVar()
        
        fft_frame = tk.IntVar()
        wave_frame = tk.IntVar()
        energy_frame = tk.IntVar()
        zcr_frame = tk.IntVar()
        corr_frame = tk.IntVar()
        amdf_frame = tk.IntVar()
        formant_frame = tk.IntVar()
        cepstral_frame = tk.IntVar()
        
        details_win = tk.Toplevel(win_name)
        details_win.title('FrameDetails')
        details_win.iconbitmap(ICON_DIR + 'icon.ico')
        
        draw_win_frame = tk.Frame(details_win, highlightbackground="black", highlightthickness=2)#,width=200, height=200)
        draw_win_frame.grid(row=1, column=0)
        
        # Signal details
        tk.Label(draw_win_frame, text='#Config').grid(row=0, column=0)
        
        tk.Label(draw_win_frame, text='Win. length (n): ').grid(row=1, column=0)
        I = tk.Entry(draw_win_frame, textvariable=win_len, width=6)
        I.insert(0, '512')
        I.grid(row=1, column=1)
        tk.Label(draw_win_frame, text='Hop (M): ').grid(row=2, column=0)
        I = tk.Entry(draw_win_frame, textvariable=hop, width=6)
        I.insert(0, '256')
        I.grid(row=2, column=1)
    
        # Pre-emphasis signal
        ttk.Radiobutton(draw_win_frame, text='Without Pre-Emph.', variable=pre_emphasis_frame_var, value='without_emphasis').grid(row=3, column=0)
        ttk.Radiobutton(draw_win_frame, text='Auto Pre-Emph.', variable=pre_emphasis_frame_var, value='auto_emphasis').grid(row=4, column=0)
        ttk.Radiobutton(draw_win_frame, text='Manual Pre-Emph.', variable=pre_emphasis_frame_var, value='manual_emphasis').grid(row=5, column=0)
        pre_emphasis_frame_var.set('without_emphasis')
        tk.Label(draw_win_frame, text='Alpha: ').grid(row=5, column=1)
        I = tk.Entry(draw_win_frame, textvariable=alpha, width=6)
        I.insert(0, '0.9')
        I.grid(row=5, column=2)
        
        # signal Window
        window_dict = {'Rectangular':ssw.boxcar, 'Hann':ssw.hann, 'Hamming':ssw.hamming}
        tk.Label(draw_win_frame, text='Windowing: ').grid(row=8, column=0)
        com_window = ttk.Combobox(draw_win_frame, textvariable=sig_window, width=10)
        com_window['values'] = list(window_dict.keys())
        com_window['state'] = 'readonly'
        com_window.current(1) # initial to hann
        com_window.grid(row=8, column=1)
        
        # a Framed signal
        tk.Label(draw_win_frame, text='#in a frame').grid(row=17, column=0)
        
        # frame number
        tk.Label(draw_win_frame, text='Frame Num. of-to: ').grid(row=18, column=0)
        I = tk.Entry(draw_win_frame, textvariable=frame_win_num_of, width=6)
        I.insert(0, '0')
        I.grid(row=18, column=1)
        I = tk.Entry(draw_win_frame, textvariable=frame_win_num_to, width=6)
        I.insert(0, '0')
        I.grid(row=18, column=2)
        
        # wave on frame
        C = tk.Checkbutton(draw_win_frame, text = "Wave", variable = wave_frame, onvalue = 1, offvalue = 0)
        C.grid(row=19, column=0)
        
        # FFT on frame
        C = tk.Checkbutton(draw_win_frame, text = "FFT ", variable = fft_frame, onvalue = 1, offvalue = 0)
        C.grid(row=20, column=0)
        tk.Label(draw_win_frame, text='FFT (n): ').grid(row=20, column=1)
        I = tk.Entry(draw_win_frame, textvariable=n_fft, width=6)
        I.insert(0, '2048')
        I.grid(row=20, column=2)
        
        # Enargy on frame
        C = tk.Checkbutton(draw_win_frame, text = "Energy", variable = energy_frame, onvalue = 1, offvalue = 0)
        C.grid(row=21, column=0)
        
        # Enargy on frame
        C = tk.Checkbutton(draw_win_frame, text = "ZCR", variable = zcr_frame, onvalue = 1, offvalue = 0)
        C.grid(row=22, column=0)
        
        # Corrolation on frame
        C = tk.Checkbutton(draw_win_frame, text = "Corrolation", variable = corr_frame, onvalue = 1, offvalue = 0)
        C.grid(row=23, column=0)
        
        # AMDF on frame
        C = tk.Checkbutton(draw_win_frame, text = "AMDF", variable = amdf_frame, onvalue = 1, offvalue = 0)
        C.grid(row=24, column=0)
        
        # Formant on frame
        C = tk.Checkbutton(draw_win_frame, text = "Formant", variable = formant_frame, onvalue = 1, offvalue = 0)
        C.grid(row=25, column=0)
        tk.Label(draw_win_frame, text='LPC (p): ').grid(row=25, column=1)
        I = tk.Entry(draw_win_frame, textvariable=p_lpc, width=6)
        I.insert(0, '13')
        I.grid(row=25, column=2)
        
        # Cepstral on frame
        C = tk.Checkbutton(draw_win_frame, text = "Cepstral", variable = cepstral_frame, onvalue = 1, offvalue = 0)
        C.grid(row=26, column=0)
        
        # Close and Apply  
        offset = signal_time_details[0].get()
        duration = signal_time_details[1].get()      
        frame_name_dict = {'wave':wave_frame, 'fft':fft_frame, 'energy':energy_frame, 'zcr':zcr_frame, 'corrolation':corr_frame, 'amdf':amdf_frame, 'formant':formant_frame, 'cepstral':cepstral_frame}
        frame_details_dict = {'win_len':win_len, 'hop':hop, 'n_fft':n_fft, 'window':[window_dict, sig_window], 'frame_win_num_of':frame_win_num_of, 'frame_win_num_to':frame_win_num_to,
                              'pre_emphasis_sig':[pre_emphasis_frame_var, alpha], 'signal_time_details':[offset, duration], 'p_lpc':p_lpc}
        button = tk.Button(draw_win_frame, text='Apply', command=lambda window=details_win, sig_details_dict=frame_details_dict: self.FrameWinVar(window, frame_name_dict, frame_details_dict))
        button.grid(row=30, column=2)
        button = tk.Button(draw_win_frame, text='Close', command=details_win.destroy)
        button.grid(row=30, column=1)
        
        
        
    def DrawWinVar(self, window, sig_name_dict, sig_details_dict):
        print('DrawWinVar')
        #print(sig_name_dict)
        #print(sig_details_dict)
        
        sig_info = fun_signal_process('load_last_process_info')
        sig_len = sig_info[0]
        
        offset = sig_details_dict['signal_time_details'][0]
        duration = sig_details_dict['signal_time_details'][1]
        if float(offset) + float(duration) <= sig_len:
            sig_details = {'offset': offset,
                           'duration': duration}
            
            window_dict = sig_details_dict['window'][0]
            window_selected = sig_details_dict['window'][1].get()
            #print(window_selected)
            #print(window_dict[window_selected])
            
            process_win_dict = {}
            if sig_name_dict['wave'].get() == 1:
                process_win_dict['wave'] = []
            
            if sig_name_dict['mfcc'].get() == 1:
                process_win_dict['mfcc'] = [sig_details_dict['n_mfcc'].get(), sig_details_dict['win_len'].get(), sig_details_dict['n_fft'].get(), sig_details_dict['hop'].get(), window_dict[window_selected]]
             
            if sig_name_dict['spec'].get() == 1:
                process_win_dict['spec'] = [sig_details_dict['win_len'].get(), sig_details_dict['n_fft'].get(), sig_details_dict['hop'].get(), window_dict[window_selected]]
            
            if sig_name_dict['fft'].get() == 1:
                process_win_dict['fft'] = [sig_details_dict['n_fft'].get(), window_dict[window_selected], sig_details_dict['win_len'].get(), sig_details_dict['hop'].get(), sig_details_dict['frame_win_num'].get()]
                                
            if sig_details_dict['pre_emphasis_sig'][0].get() == 'auto_emphasis':
                process_win_dict['pre_emphasis_sig'] = ['auto', '']    
            elif sig_details_dict['pre_emphasis_sig'][0].get() == 'manual_emphasis':
                    process_win_dict['pre_emphasis_sig'] = ['manual', sig_details_dict['pre_emphasis_sig'][1].get()] 
            elif sig_details_dict['pre_emphasis_sig'][0].get() == 'without_emphasis':
                process_win_dict['pre_emphasis_sig'] = ['without', ''] 
                    
            if sig_name_dict['pre_emphasis_coef'].get() == 1:
                process_win_dict['pre_emphasis_coef'] = [sig_details_dict['win_len'].get(), sig_details_dict['hop'].get()]
             
            if sig_name_dict['wave_frame'].get() == 1:
                process_win_dict['wave_frame'] = [sig_details_dict['win_len'].get(), sig_details_dict['hop'].get(), sig_details_dict['frame_win_num'].get()]
                
            if sig_name_dict['pre_emphasis_frame'].get() == 1:
                process_win_dict['pre_emphasis_frame'] = [sig_details_dict['win_len'].get(), sig_details_dict['hop'].get(), sig_details_dict['frame_win_num'].get()]
            
            #print(process_win_dict)
            if len(process_win_dict) != 0:
                function.DrawSubFunction(window, process_win_dict, sig_details)
        else:
            print('error for offset and duration')
            tkinter.messagebox.showerror(title='ERROR', message='Please insert correct Offset and Duration.')
        
        
    def FrameWinVar(self, window, frame_name_dict, frame_details_dict):
        print('DrawWinVar')
        print(frame_name_dict)
        print(frame_details_dict)
        
        offset = frame_details_dict['signal_time_details'][0]
        duration = frame_details_dict['signal_time_details'][1]
        
        sig_info = fun_signal_process('load_last_process_info')
        sig_len = sig_info[0]
        if float(offset) + float(duration) > sig_len:
            tkinter.messagebox.showerror(title='ERROR', message='Please insert correct Offset and Duration.')
            return 0
        
        frame_win_num_of = frame_details_dict['frame_win_num_of'].get()
        frame_win_num_to = frame_details_dict['frame_win_num_to'].get()
        win_len = frame_details_dict['win_len'].get()
        hop = frame_details_dict['hop'].get()
        window_dict = frame_details_dict['window'][0]
        window_selected = frame_details_dict['window'][1].get()
        #print(window_selected)
        #print(window_dict[window_selected])
        sig_details = {'offset': offset, 'duration': duration, 'frame_of':frame_win_num_of, 'frame_to':frame_win_num_to, 'sig_len':sig_len,
                       'window':[window_dict[window_selected]], 'win_len':win_len, 'hop':hop}
        
        frame_of = int(frame_details_dict['frame_win_num_of'].get())
        frame_to = int(frame_details_dict['frame_win_num_to'].get())
        
        if frame_of > frame_to:
            tkinter.messagebox.showerror(title='ERROR', message='Please insert correct frame numbers.')
            return 0
        
        process_win_dict = {}
        
        # Pre-Emphasis
        if frame_details_dict['pre_emphasis_sig'][0].get() == 'auto_emphasis':
            process_win_dict['pre_emphasis_sig'] = ['auto', '']    
        elif frame_details_dict['pre_emphasis_sig'][0].get() == 'manual_emphasis':
                process_win_dict['pre_emphasis_sig'] = ['manual', frame_details_dict['pre_emphasis_sig'][1].get()] 
        elif frame_details_dict['pre_emphasis_sig'][0].get() == 'without_emphasis':
            process_win_dict['pre_emphasis_sig'] = ['without', ''] 
            
        # Wave
        if frame_name_dict['wave'].get() == 1:
            process_win_dict['wave'] = []
           
        # FFT
        if frame_name_dict['fft'].get() == 1:
            process_win_dict['fft'] = [frame_details_dict['n_fft'].get(), window_dict[window_selected], frame_details_dict['win_len'].get(), frame_details_dict['hop'].get()]
                   
        # Energy
        if frame_name_dict['energy'].get() == 1:
            process_win_dict['energy'] = [frame_details_dict['win_len'].get(), frame_details_dict['hop'].get()]
            
        # ZCR
        if frame_name_dict['zcr'].get() == 1:
            process_win_dict['zcr'] = [frame_details_dict['win_len'].get(), frame_details_dict['hop'].get()]
        
        # Auto Corrolation
        if frame_name_dict['corrolation'].get() == 1:
            process_win_dict['corrolation'] = []
            
        # AMDF
        if frame_name_dict['amdf'].get() == 1:
            process_win_dict['amdf'] = []
            
        # Formant
        if frame_name_dict['formant'].get() == 1:
            process_win_dict['formant'] = [frame_details_dict['n_fft'].get(), frame_details_dict['p_lpc'].get()]
        
        # Cepstral
        if frame_name_dict['cepstral'].get() == 1:
            process_win_dict['cepstral'] = [frame_details_dict['n_fft'].get(), window_dict[window_selected], frame_details_dict['win_len'].get(), frame_details_dict['hop'].get()]
             
            
        #print(process_win_dict)
        if len(process_win_dict) != 0:
            function.FrameSubFunction(window, process_win_dict, sig_details)
        
    def DrawClose(self, win_name):
        print('DrawClose')
        
        self.root_window.deiconify()
        win_name.destroy()
        #self.process_list_win.destroy()
         
    def ReturnGuiRootWindow(self):
        return self.root_window
    
    def test(self, window, sig_name_dict, sig_details_dict):
        print('test')
        #print(win_len.get())
        #print(n_fft.get())
        #print(hop.get())
        #print(sig_details_dict['win_len'].get(), sig_details_dict['hop'].get(), sig_details_dict['n_fft'].get())
        print(sig_details_dict['win_len'], sig_details_dict['hop'], sig_details_dict['n_fft'], sig_details_dict['n_mfcc'])
        self.DrawWinVar(window, sig_name_dict, sig_details_dict)
        #self.DrawWinVar(window, win_len, hop, n_fft)
        
    
    