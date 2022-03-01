# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 08:32:55 2021

@author: Alireza Rahmati (AR)
"""

# **********************
import subprocess
import os.path as op
import os
# **********************
from tkinter import filedialog as fd
import tkinter as tk
# **********************
import sys_file.playsound_develop.playsound as ps
import recorder
import processing
# **********************
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# **********************
import numpy as np
# **********************

#system_dir_name = 'record_file.wav'

audio = recorder.AudioRecorder('sys_file/system_file.wav')
sig_process = processing.Process()

class Function:
    def __init__(self, copy_dir):
        self.save_dir = ''
        self.copy_dir = copy_dir
        #self.gui_root = gui_root
    
        self.recorded_flag = False # if recorded file this flag set to True and open_file_flag set to False
        self.opend_file_flag = False # if load file this flag set to True and recoreded_flag set to False
        
        self.play_flag = False # when play file this flag set to True
        
        self.player_class = 0
        
        audio_init = self.ReturnAudioInit()
        self.audio_format = audio_init['audio_format']
        self.audio_channels = audio_init['channels']
        self.audio_rate = audio_init['rate']
        
        self.process_figure = 0
        self.process_ax = 0
        self.process_plot_win = 0
        self.save_process_info = 0
        
        self.window_name = 0
        
        print('Function configed')
        
    def CopyFile(self, from_dir, to_dir):
        from_dir = os.path.realpath(from_dir)
        to_dir = os.path.realpath(to_dir)
        try:
            command = 'copy ' + from_dir + ' ' + to_dir
            print(command)
            result = subprocess.check_output(command , shell=True).decode('utf-8')
            print('result = ' + result)
            return True
        except subprocess.CalledProcessError:
            print('error to copy')  
            self.ShowStatus('ERROR')
            return False
        
    def SubFunction(self, sub_fun_name):
        print(sub_fun_name)
        
        # open file
        if sub_fun_name == 'open_file':
            self.save_dir = fd.askopenfilename(filetypes=[('wav files', '*.wav')])
            print(self.save_dir)
            
            if self.player_class != 0:
                self.player_class.close()  
                
            if self.CopyFile(self.save_dir, self.copy_dir) == True:
                print('file run')
                self.ShowStatus('File opend')
                
                tk.messagebox.showinfo(title='Selected File', message = self.save_dir)
                
                self.recorded_flag = False
                self.opend_file_flag = True
            else:
                tk.messagebox.showerror(title='ERROR', message = 'system can\'t run file \r\nPlease restart program')
            #wait(time_s=1)
            
        # save file
        elif sub_fun_name == 'save_file':
            if self.opend_file_flag == True:
                print(self.save_dir)
                
                if self.CopyFile(self.copy_dir, self.save_dir) == True:
                    print('file saved')
                    self.ShowStatus('File saved')
                    
                    tk.messagebox.showinfo(title='Saved File', message = self.save_dir)
                    
                else:
                    tk.messagebox.showerror(title='ERROR', message = 'system can\'t copy file \r\nPlease restart program')
                    self.ShowStatus('ERROR')
                    
            else:
                tk.messagebox.showwarning(title='Warning', message = 'Please load file or use \'save as\' for save recorded file')
                print('file didn\'t save')
                self.ShowStatus('ERROR')
                
        # save file as
        elif sub_fun_name == 'save_file_as':
            try:
                self.save_dir = fd.asksaveasfilename()
                print(self.save_dir)
                
                self.recorded_flag = False
                self.opend_file_flag = True

                if self.CopyFile(self.copy_dir, self.save_dir) == True:
                    print('file saved')
                    self.ShowStatus('File saved as ...')
                else:
                    tk.messagebox.showerror(title='ERROR', message = 'system can\'t copy file \r\nPlease restart program')
                    
                tk.messagebox.showinfo(title='Saved File', message = self.save_dir)
            except TypeError:
                print('File didn\'t save')
                self.ShowStatus('ERROR')
                
                tk.messagebox.showwarning(title='Warning', message = 'Please load file or use \'save as\' for save recorded file')
       
        # play the voice or file
        elif sub_fun_name == 'play_file':
            if self.opend_file_flag == True or self.recorded_flag == True:
                if op.isfile(self.copy_dir):
                    self.player_class = ps._music(self.copy_dir, -1)
                    self.player_class.play()
                    self.play_flag = True
                    self.ShowStatus('Play')
                else:
                    print('play error')
                    self.ShowStatus('ERROR')
                    
                    tk.messagebox.showwarning(title='Warning', message = 'error')
            else:
                tk.messagebox.showwarning(title='Warning', message = 'please load file')
                self.ShowStatus('Can\'t to load')
                
        # pause the voice
        elif sub_fun_name == 'pause_file':
            if self.play_flag == True:
                self.player_class.pause()
                self.play_flag = False
                
                self.ShowStatus('Pause')
            else:
                tk.messagebox.showwarning(title='Warning', message='Please play file...')
                self.ShowStatus('Can\'t to Play')

        # resume the voice     
        elif sub_fun_name == 'resume_file':
            if self.play_flag == False:
                self.player_class.resume()
                self.play_flag = True
                
                self.ShowStatus('Resume')
        
        # stop the voice
        elif sub_fun_name == 'stop_file':
            if self.play_flag == True:
                self.player_class.stop()
                self.play_flag = False
                
                self.ShowStatus('Stop')
                
        elif sub_fun_name == 'start_record':
            if self.player_class != 0:
                self.player_class.close()  
            audio.RecordStart()
            self.ShowStatus('Recording...')
            
        elif sub_fun_name == 'pause_record':
            audio.RecordPause()
            self.ShowStatus('Record pause')
            
        elif sub_fun_name == 'resume_record':
            audio.RecordResume()
            self.ShowStatus('Record resume')
            
        elif sub_fun_name == 'stop_record':
            audio.RecordStop()
            self.opend_file_flag = False 
            self.recorded_flag = True
            self.ShowStatus('Record stoped')
            
        elif sub_fun_name == 'about':
            print('about')
            print('Creator: #AR - Alireza')
            tk.messagebox.showinfo(title='About', message='Creator: Alireza (AR)\r\n' +
                                   ' * This is my project\r\n' +
                                   ' * My Email: AlirezaRahmati@aut.ac.com\r\n' + 
                                   ' * You can find tihs project on my Github\r\n' + 
                                   ' * V1.3')
                
        else:
            print('ERROR for ' + sub_fun_name)
            self.ShowStatus('Function ERROR')
            
    def Properties(self, window_name, com_format, com_channels, ent_rate):
        self.recorded_flag = False # disable recorded file
        self.opend_file_flag = False # disable opend file
        self.ShowStatus('Empty')
        
        pro_ok_flag = True
        
        print(com_format.get())
        print(com_channels.get())
        print(ent_rate.get())
        
        if com_format.get() == '8bit':
            audio_format = 16
        elif com_format.get() == '16bit':
            audio_format = 8
        elif com_format.get() == '32bit':
            audio_format = 2
        else:
            print('error for com_format')
            print('format set to 16bit')
            audio_format = 8
            
        if com_channels.get() == 'mono':
            channels = 1
        elif com_channels.get() == 'sterio':
            channels = 2
        else:
            print('error for com_channels')
            print('channels set to mono')
            channels = 1
            
        if int(ent_rate.get())>=8000 and int(ent_rate.get())<=36000:
            rate = int(ent_rate.get())
        else:
            print('rate must be between 8000 to 36000')
            print('rate set to 16000')
            pro_ok_flag = False
        
        if pro_ok_flag == True:
            
            # You should use pyaudio.paInt8 (16) or pyaudio.paInt16 (8) or pyaudio.paInt32 (2) for audio_format
            # self.channel should set to 1 or 2
            audio.RecorderInit(audio_format, channels, rate)
            print('audio configed:')
            print(audio.RecorderReadInit())
            
            window_name.destroy()
        else:
            tk.messagebox.showerror(title='ERROR', message = 'Rate must be between 8000 to 36000\r\nRate set to 16000')
            print('error on properties')
            print(audio.RecorderReadInit())
            
    def ShowStatusInit(self, window_name, x_grid, y_grid, status_text='Empty'):
        self.status_window = window_name
        self.status_x_grid = x_grid
        self.status_y_grid = y_grid
        
        tk.Label(self.status_window, text='Status: ').grid(row=self.status_x_grid, column=self.status_y_grid)
        self.status_label = tk.Label(self.status_window, text=status_text)
        self.status_label.grid(row=self.status_x_grid, column=self.status_y_grid+20)
        
    def ShowStatus(self, status_text):
        self.status_label.destroy()
        tk.Label(self.status_window, text='Status: ').grid(row=self.status_x_grid, column=self.status_y_grid)
        self.status_label = tk.Label(self.status_window, text=status_text)
        self.status_label.grid(row=self.status_x_grid, column=self.status_y_grid+20)
            
    def ReturnAudioInit(self):
        return audio.RecorderReadInit()
    
    def SaveAudioInit(self):
        audio_init = self.ReturnAudioInit()
        self.audio_format = audio_init['audio_format']
        self.audio_channels = audio_init['channels']
        self.audio_rate = audio_init['rate']
        
    def ProseccingSubFun(self, sub_process_name):
        print('process - ' + sub_process_name)
        
        self.SaveAudioInit()
        
        # process load
        if sub_process_name == 'process_load':
            if self.recorded_flag == True or self.opend_file_flag == True:
                sig_process.LoadSig(self.copy_dir, self.audio_rate, self.audio_channels)
                print('load to process')
            else:
                print('please load file')
                self.ShowStatus('Please load file')
                tk.messagebox.showerror(title='Error', message='No file.')
                
        # Process info
        elif sub_process_name == 'process_info':
            self.save_process_info = sig_process.LengthSig()
            return self.save_process_info
        
        elif sub_process_name == 'load_last_process_info':
            return self.save_process_info
                
        elif sub_process_name == 'process_draw':
            print('wave')
            
            self.process_ax = 0
            if self.process_ax == 0:
                self.CreateFigure(5, 5)
                
            sig_process.WaveDraw(self.process_ax)
            
            self.CreatePlotWin()
            self.ShowFigure(self.process_plot_win)
            
            self.ShowStatus('Draw wave')
            
                
        elif sub_process_name == 'process_mfcc':
            print('mfcc')
            
            if self.recorded_flag == True or self.opend_file_flag == True:
                sig_process.LoadFile(self.copy_dir, self.audio_rate, self.audio_channels)
                
                self.process_ax = 0
                if self.process_ax == 0:
                    self.CreateFigure(5, 5)
                    
                sig_process.MFCC(40, self.process_figure, self.process_ax)
                
                self.CreatePlotWin()
                self.ShowFigure(self.process_plot_win)
                
                self.ShowStatus('Draw MFCC')
            else:
                print('please load file')
                self.ShowStatus('Please load file')
                
        else:
            print('process name error - ' + sub_process_name)
            
    def DrawSubFunction(self, window, process_dict, sig_info):
        print('DrawSubFunction')
        details = '                          '
        details += 'Details: ' # for show details in the window
       
        
        print(process_dict)
        print(sig_info)
        
        if self.recorded_flag == True or self.opend_file_flag == True:
            offset = float(sig_info['offset'])
            duration = float(sig_info['duration'])
            sig_process.LoadSig(self.copy_dir, self.audio_rate, self.audio_channels, offset=offset, duration=duration)
            
            # signal Auto pre-emphassis
            if process_dict['pre_emphasis_sig'][0] == 'manual':
                print('Manual-SignalPre-Emphsis')               
                
                if self.audio_channels == 1:
                    sig_process.ApplyPreEmpasisToSig(alpha = float(process_dict['pre_emphasis_sig'][1]), channel=1)
                elif self.audio_channels == 2:
                    sig_process.ApplyPreEmpasisToSig(alpha = float(process_dict['pre_emphasis_sig'][1]), channel=2)
            # Delete Auto Pre-Emphasis of drawing list
            
            elif process_dict['pre_emphasis_sig'][0] == 'auto':
                print('Auto-SignalPre-Emphsis')  
                
                ( _ , alpha) = sig_process.AutoPreEmpasisToSig(channel=self.audio_channels-1)
                details += 'Pre-Emphasis coef.={:.2f}, '.format(alpha)
                
            del process_dict['pre_emphasis_sig']

            # Draw signal
            if process_dict != {}:
                fig = Figure(figsize=(10,7), dpi=100)
                fig.subplots_adjust(hspace=1.6)
                
                details += ('Offset={} S, Duration={} S'.format(sig_info['offset'], sig_info['duration']))
                details += '                          '
                draw_num = len(process_dict)
                
                if self.audio_channels == 2: # sterio
                    draw_num*=2
                i = 1
                for name in process_dict.keys():
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    
                    # Wave
                    if name == 'wave':
                        ax.set_ylabel('Amp.')
                        sig_process.WaveDraw(ax)
                        
                        if self.audio_channels == 2:
                            ax = fig.add_subplot(draw_num, 1, i)
                            i += 1
                            sig_process.WaveDraw(ax, channel=2)
                        
                    # MFCC
                    elif name == 'mfcc':
                        ax.set_ylabel('Mag.')
                        sig_process.MFCC(int(process_dict['mfcc'][0]), fig, ax, int(process_dict['mfcc'][2]), int(process_dict['mfcc'][1]), int(process_dict['mfcc'][3]), window=process_dict['mfcc'][4])
                        
                        if self.audio_channels == 2:
                            ax = fig.add_subplot(draw_num, 1, i)
                            i += 1
                            sig_process.MFCC(int(process_dict['mfcc'][0]), fig, ax, int(process_dict['mfcc'][2]), int(process_dict['mfcc'][1]), int(process_dict['mfcc'][3]), channel=2, window=process_dict['mfcc'][4])
                            
                    # Sectrogram
                    elif name == 'spec':
                        sig_process.Spectrogram(fig, ax, int(process_dict['spec'][1]), int(process_dict['spec'][0]), int(process_dict['spec'][2]), window=process_dict['spec'][3])
                        
                        if self.audio_channels == 2:
                            ax = fig.add_subplot(draw_num, 1, i)
                            i += 1
                            sig_process.Spectrogram(fig, ax, int(process_dict['spec'][1]), int(process_dict['spec'][0]), int(process_dict['spec'][2]), channel=2, window=process_dict['spec'][3])
                
                    # Pre-Emphasis
                    elif name == 'pre_emphasis_coef':
                        frames = sig_process.Framming(int(process_dict['pre_emphasis_coef'][0]), int(process_dict['pre_emphasis_coef'][1]))
                        sig_process.PreEmphasis(frames, ax)
                        
                        if self.audio_channels == 2:
                            ax = fig.add_subplot(draw_num, 1, i)
                            i += 1
                            frames = sig_process.Framming(int(process_dict['pre_emphasis_coef'][0]), int(process_dict['pre_emphasis_coef'][1]), channel=2)
                            sig_process.PreEmphasis(frames, ax)
                        
                    # FFT
                    elif name == 'fft':
                        framed_signal = sig_process.Framming(int(process_dict['fft'][2]),int(process_dict['fft'][3]))
                        frame_win_num = int(process_dict['fft'][4])

                        sig_process.FFT(framed_signal[:,frame_win_num], ax, int(process_dict['fft'][0]), window=process_dict['fft'][1], sample_rate=self.audio_rate)
                        
                        if self.audio_channels == 2:
                            ax = fig.add_subplot(draw_num, 1, i)
                            i += 1
                            
                            framed_signal = sig_process.Framming(int(process_dict['fft'][2]),int(process_dict['fft'][3]), channel=2)
                            frame_win_num = int(process_dict['fft'][4])

                            sig_process.FFT(framed_signal[1:,frame_win_num], ax, int(process_dict['fft'][0]), window=process_dict['fft'][1], sample_rate=self.audio_rate)
                                
                    # Pre_emphasis frame
                    elif name == 'pre_emphasis_frame':
                        framed_signal = sig_process.Framming(int(process_dict['pre_emphasis_frame'][0]),int(process_dict['pre_emphasis_frame'][1]))
                        frame_win_num = int(process_dict['pre_emphasis_frame'][2])
                        
                        sig_frame = framed_signal[:,frame_win_num]
                        sig_frame = np.expand_dims(sig_frame, -1)

                        sig_frame = sig_process.AutoPreEmpasisToFrame(sig_frame, channel=1)

                        # Wave new frame
                        sig_process.WaveFrame(sig_frame, ax)
                        
                        if self.audio_channels == 2:
                            framed_signal = sig_process.Framming(int(process_dict['pre_emphasis_frame'][0]),int(process_dict['pre_emphasis_frame'][1]), channel=2)
                            frame_win_num = int(process_dict['pre_emphasis_frame'][2])
                            
                            sig_frame = framed_signal[:,frame_win_num]
                            sig_frame = np.expand_dims(sig_frame, -1)
                            
                            ax = fig.add_subplot(draw_num, 1, i)
                            i += 1
                            sig_process.WaveFrame(sig_frame, ax)
                       
                    # Wave in frame
                    elif name == 'wave_frame':
                        framed_signal = sig_process.Framming(int(process_dict['wave_frame'][0]), int(process_dict['wave_frame'][1]))
                        frame_win_num = int(process_dict['wave_frame'][2])
                        sig_process.WaveInFrame(framed_signal[:,frame_win_num], ax)
                        
                        if self.audio_channels == 2:
                            ax = fig.add_subplot(draw_num, 1, i)
                            i += 1
                            framed_signal = sig_process.Framming(int(process_dict['wave_frame'][0]), int(process_dict['wave_frame'][1]), channel=2)
                            frame_win_num = int(process_dict['wave_frame'][2])
                            sig_process.WaveInFrame(framed_signal[:,frame_win_num], ax)
                            
                        
                #process_plot_win = tk.Toplevel(self.window_name)
                process_plot_win = window
                
                # Show detials
                tk.Label(process_plot_win, text=details).grid(row=0, column=3)
                
                # show draw
                canvas = FigureCanvasTkAgg(fig, master=process_plot_win)
                canvas.draw()
                
                canvas.get_tk_widget().grid(row=1, column=3)
                
                toolbar_fram = tk.Frame(process_plot_win)
                toolbar_fram.grid(row=2, column=3)
                toolbar = NavigationToolbar2Tk(canvas, toolbar_fram)
                toolbar.update()

        else:
            print('please load file')
            self.ShowStatus('Please load file')
             
    def FrameSubFunction(self, window, process_dict, sig_info):
        print('FrameSubFunction')
        details = '                          '
        details += 'Details: ' # for show details in the window
       
        print(process_dict)
        print(sig_info)
        
        # check and load signal
        if self.recorded_flag == True or self.opend_file_flag == True:
            #sig_offset = float(sig_info['offset'])
            #sig_duration = float(sig_info['duration'])
            
            # frame lenght
            frame_of = int(sig_info['frame_of'])
            frame_to = int(sig_info['frame_to'])
            n = frame_to - frame_of + 1
            win_len = int(sig_info['win_len'])
            hop = int(sig_info['hop'])
            new_duration = (n * win_len) - (win_len - hop) * (n - 1)
            new_offset = (frame_of * hop)
            sig_duration = float(sig_info['duration']) * self.audio_rate
            
            FRAME_ERROR_FLAG = False
            if (new_duration + new_offset) > sig_duration:
                new_duration = sig_duration - new_offset
                FRAME_ERROR_FLAG = True
                
            new_duration  /= self.audio_rate
            new_offset  /= self.audio_rate
            print('frames: new_offset = {}s, new_duration = {}s'.format(new_offset, new_duration))
            sig_data = sig_process.LoadSig(self.copy_dir, self.audio_rate, self.audio_channels, offset=new_offset, duration=new_duration)
            # sig_data.shape = (channel, num)
            
        else:
            print('please load file')
            self.ShowStatus('Please load file')
            tk.messagebox.showerror(title='ERROR', message = 'Please load file')
            return 0
        
        # signal Auto pre-emphassis
        if process_dict['pre_emphasis_sig'][0] == 'manual':
            print('Manual-SignalPre-Emphsis')               
            
            if self.audio_channels == 1:
                sig_process.ApplyPreEmpasisToSig(alpha = float(process_dict['pre_emphasis_sig'][1]), channel=1)
            elif self.audio_channels == 2:
                sig_process.ApplyPreEmpasisToSig(alpha = float(process_dict['pre_emphasis_sig'][1]), channel=2)
        
        elif process_dict['pre_emphasis_sig'][0] == 'auto':
            print('Auto-SignalPre-Emphsis')  
            
            ( _ , alpha) = sig_process.AutoPreEmpasisToSig(channel=self.audio_channels-1)
            details += 'Pre-Emphasis coef.={:.2f}, '.format(alpha)
            
        # Delete Auto Pre-Emphasis of drawing list
        del process_dict['pre_emphasis_sig']
        
        if process_dict == {}:
            tk.messagebox.showerror(title='ERROR', message = 'Please select a option')
            return 0
        
        # Draw info
        fig = Figure(figsize=(10,7), dpi=100)
        fig.subplots_adjust(hspace=1.6)
        
        details += ('Offset={} + {} S, Duration={} S, num. of frames={}'.format(sig_info['offset'], new_offset, new_duration, n))
        
        if FRAME_ERROR_FLAG == True:
            details += (', Error on frame numbers')
        
        details += '                                       '
        draw_num = len(process_dict)
        
        if self.audio_channels == 2: # sterio
            draw_num*=2
        i = 1
        for name in process_dict.keys():
            ax = fig.add_subplot(draw_num, 1, i)
            i += 1
            
            # Wave
            if name == 'wave':
                ax.set_ylabel('Amp.')
                sig_process.WaveDraw(ax)
                
                if self.audio_channels == 2:
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    sig_process.WaveDraw(ax, channel=2)
        
            # FFT
            elif name == 'fft':
                sig_process.FFT(sig_data[0,:], ax, int(process_dict['fft'][0]), window=process_dict['fft'][1], sample_rate=self.audio_rate)
                
                if self.audio_channels == 2:
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    
                    sig_process.FFT(sig_data[1,:], ax, int(process_dict['fft'][0]), window=process_dict['fft'][1], sample_rate=self.audio_rate)
            
            # Energy
            elif name == 'energy':
                framed_sig = sig_process.Framming(int(process_dict['energy'][0]), int(process_dict['energy'][1]))
                energies = []
                for frame_num in range(framed_sig.shape[1]):
                    energies.append(sig_process.getEnergy(framed_sig[:, frame_num]))
                    
                sig_process.ScatterX(ax, y=energies, xlabel='Frames', ylabel='Energies')
                
                if self.audio_channels == 2:
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    
                    framed_sig = sig_process.Framming(int(process_dict['energy'][0]), int(process_dict['energy'][1]))
                    energies = []
                    for frame_num in range(framed_sig.shape[1]):
                        energies.append(sig_process.getEnergy(framed_sig[:, frame_num]))
                        
                    sig_process.ScatterX(ax, y=energies, xlabel='Frames', ylabel='Energies')
                    
            # ZCR
            elif name == 'zcr':
                framed_sig = sig_process.Framming(int(process_dict['zcr'][0]), int(process_dict['zcr'][1]))
                zcr = []
                for frame_num in range(framed_sig.shape[1]):
                    zcr.append(sig_process.getZCR(framed_sig[:, frame_num]))
                    
                #sig_process.ScatterX(ax, y=zcr, xlabel='Frames', ylabel='ZCR', show_location=True)
                sig_process.ScatterX(ax, y=zcr, xlabel='Frames', ylabel='ZCR')
                
                if self.audio_channels == 2:
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    
                    framed_sig = sig_process.Framming(int(process_dict['zcr'][0]), int(process_dict['zcr'][1]))
                    zcr = []
                    for frame_num in range(framed_sig.shape[1]):
                        zcr.append(sig_process.getZCR(framed_sig[:, frame_num]))
                        
                    #sig_process.ScatterX(ax, y=zcr, xlabel='Frames', ylabel='ZCR', show_location=True)
                    sig_process.ScatterX(ax, y=zcr, xlabel='Frames', ylabel='ZCR')
                    
            # Auto Corrolation
            elif name == 'corrolation':
                auto_corr = []
                for eta in range(sig_data.shape[1]):
                    auto_corr.append(sig_process.getCORR(sig_data[0,:], eta))
                #print(auto_corr)
                sig_process.PlotX(ax, y=auto_corr, ylabel='Auto Corrolation')
                
                if self.audio_channels == 2:
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    
                    auto_corr = []
                    for eta in range(sig_data.shape[1]):
                        auto_corr.append(sig_process.getCORR(sig_data[1,:], eta))
                    #print(auto_corr)
                    sig_process.PlotX(ax, y=auto_corr, ylabel='Auto Corrolation')
                    
            # AMDF
            elif name == 'amdf':
                amdf = []
                for eta in range(sig_data.shape[1]):
                    amdf.append(sig_process.getAMDF(sig_data[0,:], eta))
                sig_process.PlotX(ax, y=amdf, ylabel='AMDF')
                
                if self.audio_channels == 2:
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    
                    amdf = []
                    for eta in range(sig_data.shape[1]):
                        amdf.append(sig_process.getAMDF(sig_data[1,:], eta))
                    sig_process.PlotX(ax, y=amdf, ylabel='AMDF')
                
            # Formant
            elif name == 'formant':
                n_fft = int(process_dict['formant'][0])
                p = int(process_dict['formant'][1])
                (x_lpc, x_fft) = sig_process.getFormant(sig_data[0,:], p, n_fft)
                x = np.linspace(0, self.audio_rate//2, n_fft//2)
                
                sig_process.PlotXY(ax, x, y=x_lpc[:n_fft//2], legend='with LPC')
                sig_process.PlotXY(ax, x, y=x_fft[:n_fft//2], legend='with FFT', xlabel='freq Hz')
                
                if self.audio_channels == 2:
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    
                    (x_lpc, x_fft) = sig_process.getFormant(sig_data[1,:], p, n_fft)
                    sig_process.PlotXY(ax, x, y=x_lpc[:n_fft//2], legend='with LPC')
                    sig_process.PlotXY(ax, x, y=x_fft[:n_fft//2], legend='with FFT', xlabel='freq Hz')
            
            # Cepstral
            elif name == 'cepstral':
                ceps = sig_process.getCepstral(sig_data[0,:], int(process_dict['cepstral'][0]), window=process_dict['cepstral'][1], sample_rate=self.audio_rate)
                sig_process.PlotX(ax, y=ceps, ylabel='Cepstral')
                if self.audio_channels == 2:
                    ax = fig.add_subplot(draw_num, 1, i)
                    i += 1
                    
                    ceps = sig_process.getCepstral(sig_data[1,:], int(process_dict['cepstral'][0]), window=process_dict['cepstral'][1], sample_rate=self.audio_rate)
                    sig_process.PlotX(ax, y=ceps, ylabel='Cepstral')
                
        #process_plot_win = tk.Toplevel(self.window_name)
        process_plot_win = window
        
        # Show detials
        tk.Label(process_plot_win, text=details).grid(row=0, column=3)
        
        # show draw
        canvas = FigureCanvasTkAgg(fig, master=process_plot_win)
        canvas.draw()
        
        canvas.get_tk_widget().grid(row=1, column=3)
        
        toolbar_fram = tk.Frame(process_plot_win)
        toolbar_fram.grid(row=2, column=3)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_fram)
        toolbar.update()
    
    
    def MainWinName(self, window_name):
        self.window_name = window_name

# Test
#my_fun = Function('', '')
#my_fun.SubFunction('play_file')
            
            
            
    