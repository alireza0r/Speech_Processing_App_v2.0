# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 20:03:25 2021

@author: Alireza Rahmati (AR)

* Thanks of Taylor Marks <taylor@marksfam.com> for playsound.py lib.
* His git hub : https://github.com/TaylorSMarks/playsound

"""
# *******************
import platform
import sys
# *******************

def main():
    # *******************
    import gui
    import tkinter as tk
    # *******************
    
    root = tk.Tk()
    my_gui = gui.Gui(root)
    my_gui.RunGui()
    root.mainloop()
    
    print('Exit')
    
if __name__ == '__main__':
    print('Note: You must use the Windows')
    print('your platform: ' + platform.platform())
    sys.exit(main())
