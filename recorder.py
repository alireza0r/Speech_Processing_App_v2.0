# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:46:41 2021

@author: Alireza Rahmati (AR)
"""

# *******************
import pyaudio
import wave
# *******************
import os
# *******************

'''
audio record function
'''
class AudioRecorder:
    def __init__(self, file_dir):
        self.file_dir = file_dir
        
        self.fulldata = []
        
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        
        self.audio_class = 0 # pyaudio.PyAudio()
        self.stream = ''
        
        print('Recorder config')
    
    def CallBack(self, in_data, frame_count, time_info, flag):
        self.fulldata.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def RecorderInit(self, format, channels, rate):
        self.format = format
        self.channels = channels
        self.rate = rate
    
    def Clear(self):
        self.fulldata = []
    
    def RecordStart(self):
        if os.path.exists(self.file_dir):
            try:
                os.remove(self.file_dir)
            except:
                print('error while recording')
                return False
            
        self.Clear()
        
        self.audio_class = pyaudio.PyAudio()
        self.stream = self.audio_class.open(format=self.format, channels=self.channels, rate=self.rate, input=True, stream_callback=self.CallBack)
        self.stream.start_stream()
        return True
        
    def RecordPause(self):
        self.stream.stop_stream()
        self.stream.close()
        
    def RecordResume(self):
        if self.audio_class != 0:
            self.stream = self.audio_class.open(format=self.format, channels=self.channels, rate=self.rate, input=True, stream_callback=self.CallBack)
            self.stream.start_stream()
    
    def RecordStop(self):
        if self.audio_class != 0:
            self.stream.stop_stream()
            self.stream.close()
            self.audio_class.terminate()
            
            sound_file = wave.open(self.file_dir, "wb")
            sound_file.setnchannels(self.channels)
            sound_file.setsampwidth(self.audio_class.get_sample_size(self.format))
            sound_file.setframerate(self.rate)
    
            sound_file.writeframes(b''.join(self.fulldata))
            sound_file.close()
            
            print('rcord stoped, samples={}x1024'.format(len(self.fulldata)))
    
    def RecordDetails(self):
        print('****************************************')
        print('Data len = ' + str(len(self.fulldata)))
        print('file dir: ' + self.file_dir)
        print('****************************************')
        
    def RecorderInit(self, audio_format, channels, rate):
        self.format = audio_format
        self.channels = channels
        self.rate = rate
        
    # You should use pyaudio.paInt8 (16) or pyaudio.paInt16 (8) or pyaudio.paInt32 (2) for self.format
    # self.channel should set to 1 or 2
    def RecorderReadInit(self):
        return {'audio_format':self.format, 'channels':self.channels, 'rate':self.rate}
        

# Test
'''
print('record started')
audio = AudioRecorder('record_file.wav')
audio.RecordStart()
time.sleep(20)
audio.RecordStop()
audio.RecordDetails()
'''