"""
Project title: IGMW API client application (GUI)
Author: Piotr Frydman
"""

import tkinter as tk

class imgwApiGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IMGW Api Client")
        self.geometry("600x400+500+250")
        self.resizable(False, False)
        
        #położenie elementów w oknie
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=3)
        
        
apiClient = imgwApiGui()
apiClient.mainloop()
