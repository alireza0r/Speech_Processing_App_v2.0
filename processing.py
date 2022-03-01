# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 12:04:22 2021

@author: Alireza Rahmati (AR)
"""
import librosa
import librosa.display
import numpy as np
import scipy.signal.windows as ssw
import scipy.fft as sf

class Process:
    def __init__(self):
        self.wave_file_dir = ''
        self.signal_data = 0
        self.rate = 16000
        self.channels = 1
        
        print('Process config')
    
    def LoadSig(self, wave_file_dir, rate, channels, offset=0.0, duration=None):
        self.wave_file_dir = wave_file_dir
        self.channels = channels
        
        if self.channels == 1:
            mono = True
        else:
            mono = False
        
        self.signal_data, self.rate = librosa.load(self.wave_file_dir, sr=rate, mono=mono, offset=offset, duration=duration)
        print('signal loaded, shape={}'.format(self.signal_data.shape))
        
        if channels == 1:
            self.signal_data = np.expand_dims(self.signal_data, 0) 

        return self.signal_data
        
    def LengthSig(self):
        return (self.signal_data.shape[-1] / float(self.rate), self.signal_data.shape[-1])
        
    def WaveDraw(self, ax, channel=1):
        if channel == 1:
            librosa.display.waveplot(self.signal_data[0,:], sr=self.rate, ax=ax)
            ax.set_ylabel('Amplitude')
            ax.set_title('Wave')
        elif channel == 2:
            librosa.display.waveplot(self.signal_data[1,:], sr=self.rate, ax=ax)
            ax.set_ylabel('Amplitude')
            #ax.set_title('Wave (channel 2)')
        else:
            return False
        
    def WaveInFrame(self, frame, ax):
        print(frame.shape)
        librosa.display.waveplot(frame, sr=self.rate, ax=ax)
        ax.set_ylabel('Amplitude')
        ax.set_title('Wave in a frame')
        
    def MFCC(self, n_mfcc, figure, ax, n_fft=2048, win_length=512, hop_length=512, channel=1, window='hann'):
        if channel == 1:
            mfcc = librosa.feature.mfcc(self.signal_data[0,:], sr=self.rate, n_mfcc=n_mfcc, n_fft=n_fft, win_length=win_length, hop_length=hop_length)
            img = librosa.display.specshow(mfcc, sr=self.rate, x_axis='frames', ax=ax)
            figure.colorbar(img, ax=ax)
            ax.set_ylabel('Coef.')
            ax.set_title('MFCC')
        elif channel == 2:
            mfcc = librosa.feature.mfcc(self.signal_data[1,:], sr=self.rate, n_mfcc=n_mfcc, n_fft=n_fft, win_length=win_length, hop_length=hop_length, window=window)
            img = librosa.display.specshow(mfcc, sr=self.rate, x_axis='frames', ax=ax)
            figure.colorbar(img, ax=ax)
            ax.set_ylabel('Coef.')
            #ax.set_title('MFCC (channel 2)')
        else:
            return False
        
    def Spectrogram(self, figure, ax, n_fft=2048, win_length=512, hop_length=512, channel=1, window='hann'):
        if channel == 1:
            freqs, times, mags = librosa.reassigned_spectrogram(self.signal_data[0,:], sr=self.rate, n_fft=n_fft, win_length=win_length, hop_length=hop_length, window=window)
            mags = librosa.amplitude_to_db(mags, ref=np.max)
            img = librosa.display.specshow(mags, sr=self.rate, x_axis='frames', y_axis='linear', ax=ax)
            figure.colorbar(img, ax=ax)
            ax.set_title('Spectrogram')
        elif channel == 2:
            freqs, times, mags = librosa.reassigned_spectrogram(self.signal_data[1,:], sr=self.rate, n_fft=n_fft, win_length=win_length, hop_length=hop_length)
            img = librosa.display.specshow(mags, sr=self.rate, x_axis='frames', y_axis='linear', ax=ax)
            figure.colorbar(img, ax=ax)
            #ax.set_title('Spectrogram (channel 2)')
        else:
            return False

    def Framming(self, frame_length, hop, channel=1):
        print('framing')
        
        if channel == 1 or channel == 2:
            # Zero Padding          
            if self.signal_data.shape[-1] % hop != 0:
                sig_new_len = int(np.ceil(self.signal_data.shape[-1] / hop))
                sig_new_len *= hop
                
                dif = sig_new_len - self.signal_data.shape[-1]
                print(f'diff={dif}')
                
                new_sig = np.pad(self.signal_data[channel-1,:], (0, dif), 'constant', constant_values=(0))
            else:
                new_sig = self.signal_data[channel-1,:]
               
            return librosa.util.frame(new_sig, frame_length=frame_length, hop_length=hop)
        else:
            return False
    
    def FFT(self, signal, ax, n_fft=2048, window=ssw.hann, sample_rate=16000):
        window = window(signal.shape[-1]) 
        new_sig = signal * window

        fft = sf.fft(new_sig)

        T = 1.0/sample_rate
        N = fft.shape[0]
        
        xf = sf.fftfreq(N, T)
        xf = sf.fftshift(xf)
        yf = sf.fftshift(fft)

        fft = np.expand_dims(fft, -1)
        
        ax.set_ylabel('Mag.')
        ax.set_xlabel('Hz')
        ax.set_title('FFT')
        sig_for_draw = 20*np.log(abs(yf))
        ax.plot(xf, sig_for_draw)
        #ax.plot(xf, sig_for_draw, '-o')  
    
    # frames: shape = (samples,frames)
    # eta: Autocorrolation coffecient
    def AutocorrelationInFrame(self, frames, eta):
        print('AutocorrelationInFrame')
        print(frames.shape)
        corrolation_list = []
        
        for frame in range(frames.shape[-1]):
            s = frames[:, frame]
            sig_len = frames.shape[0]
            s_eta = np.zeros(shape=sig_len)
            
            s = np.expand_dims(s, 0)
            s_eta = np.expand_dims(s_eta, 0)
            
            # shift
            s_eta[0, :sig_len - eta] = s[0, eta:]
            
            corrolation_list.append(np.dot(s, s_eta.T) / float(sig_len))
        return np.squeeze(np.array(corrolation_list))
    
    def PreEmphasis(self, frames, ax):
        r0 = self.AutocorrelationInFrame(frames, 0)
        r1 = self.AutocorrelationInFrame(frames, 1)
        alpha = r1/r0
        
        ax.set_ylabel(r'$\alpha$')
        ax.set_xlabel('frames')
        ax.set_title('Pre-Emphasis Coef.')
        ax.grid()
        ax.scatter(np.arange(alpha.shape[0]), alpha)
        
        for i, text in enumerate(alpha):
            ax.annotate('[{},{:.2f}]'.format(i, text), (i, text))
        return alpha
    
    def ApplyPreEmpasisToSig(self, alpha, channel=1):
        if channel == 1:
            self.signal_data[0,:] = librosa.effects.preemphasis(self.signal_data[0,:], alpha)
            return self.signal_data
        elif channel == 2:
            for i in range(2):
                self.signal_data[i,:] = librosa.effects.preemphasis(self.signal_data[i,:], alpha)
            return self.signal_data
        else:
            return False  
        
    def AutoPreEmpasisToFrame(self, frame, channel=1):
        print('AutoPreEmpasisToFrame')
        print(frame.shape)
        
        r0 = self.AutocorrelationInFrame(frame, 0)
        r1 = self.AutocorrelationInFrame(frame, 1)
        self.alpha = r1/r0
        
        if channel == 1:
            frame = librosa.effects.preemphasis(np.squeeze(frame, -1), self.alpha)
            return frame
        elif channel == 2:
            for i in range(2):
                frame = librosa.effects.preemphasis(frame, self.alpha)
            return frame
        else:
            return False  
        
    def AutoPreEmpasisToSig(self, channel=1):
        print('AutoPreEmpasisToSig')
        
        frame = self.signal_data[channel-1,:]
        
        r0 = self.AutocorrelationInFrame(np.expand_dims(frame, -1), 0)
        r1 = self.AutocorrelationInFrame(np.expand_dims(frame, -1), 1)
        alpha = r1/r0
        
        frame = librosa.effects.preemphasis(frame, alpha)
        self.signal_data[channel-1,:] = frame
        return (frame, alpha)
        
    def WaveFrame(self, frame, ax):
        librosa.display.waveplot(frame, sr=self.rate, ax=ax, label=r'$\alpha$={:.2f}'.format(self.alpha))
        ax.set_ylabel('Amplitude')
        ax.set_title('Wave for a frame')
        ax.legend()
    
    def getEnergy(self, frame):
        return np.sum(frame**2) / float(frame.shape[0])
    
    def getZCR(self, frame):
        zcr = 0
        for i in range(1, frame.shape[0]):
            zcr += np.abs(np.sign(frame[i]) - np.sign(frame[i-1])) / 2
        return zcr
    
    def getCORR(self, frame, eta):
        if eta > frame.shape[0]:
            return None
        
        auto_corr = 0
        for i in range(eta, frame.shape[0]):
            auto_corr += frame[i] * frame[i-eta]
            
        return auto_corr / float(frame.shape[0] - eta)
    
    def getAMDF(self, frame, eta):
        if eta > frame.shape[0]:
            return None
        
        amdf = 0
        for i in range(frame.shape[0]):
            if i < eta:
                #amdf += np.abs(frame[i])
                pass
            else:
                amdf += np.abs(frame[i] - frame[i-eta])
            
        return amdf / float(frame.shape[0])
    
    def getFormant(self, frame, lpc_p, n_fft):
        lpc = librosa.lpc(frame, lpc_p)
        root = np.zeros(n_fft)
        root[:lpc.shape[0]] = lpc
        a = 1 / np.abs(sf.fft(root, n_fft))
        x_lpc = 20*np.log(a)

        x_fft = 20*np.log(np.abs(sf.fft(frame,n_fft)))
        
        return (x_lpc, x_fft)
        
    def getCepstral(self, frame, n_fft=2048, window=ssw.hann, sample_rate=16000):
        window = window(frame.shape[0]) 
        new_sig = frame * window

        fft = sf.fft(new_sig)
        ceps = sf.ifft(np.log(np.abs(fft)))
        return ceps
    
    def Smoothing(self, frame, num=5):
        new_frame = np.zeros(frame.shape)
        for i in range(frame.shape[0]):
            for j in range(num):
                new_frame[i + num//2] += frame[i+j]
        return new_frame
    
    def PlotX(self, ax, y, xlabel=None, ylabel=None, title=None, legend=None):
        if xlabel != None:
            ax.set_xlabel(xlabel)
        if ylabel != None:
            ax.set_ylabel(ylabel)
        if title != None:
            ax.set_title(title)
        if legend != None:    
            ax.plot(y, label=legend)
            ax.legend()
        else:
            ax.plot(y)
    
    def PlotXY(self, ax, x, y, xlabel=None, ylabel=None, title=None, legend=None):
        if xlabel != None:
            ax.set_xlabel(xlabel)
        if ylabel != None:
            ax.set_ylabel(ylabel)
        if title != None:
            ax.set_title(title)
        if legend != None:    
            ax.plot(x, y, label=legend)
            ax.legend()
        else:
            ax.plot(x, y)
            
    def ScatterX(self, ax, y, xlabel=None, ylabel=None, title=None, legend=None, show_location=False):
        x = range(len(y))
        ax.grid(which='both')
        if xlabel != None:
            ax.set_xlabel(xlabel)
        if ylabel != None:
            ax.set_ylabel(ylabel)
        if title != None:
            ax.set_title(title)
        if legend != None:    
            ax.scatter(x, y, label=legend)
            ax.legend()
        else:
            ax.scatter(x, y)
            
        if show_location != False:
            for i, text in enumerate(y):
                ax.annotate('[{},{:.2f}]'.format(i, text), (i, text))
        
#speech_process = Process()
#speech_process.LoadFile('system_file.wav', 16000)
#speech_process.WaveDraw()