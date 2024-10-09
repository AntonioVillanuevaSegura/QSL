"""
Antonio Villanueva Segura F4LEC
Program to edit a QSL the input arguments are as follows
STATION DATE UTC MHZ RST MOD
"""
import sys #Arguments
import PIL
from PIL import ImageFont ,Image ,ImageDraw

import tkinter as tk #Gui
from tkinter import ttk
from tktooltip import ToolTip #infobulles
from tkinter import filedialog

import os
import sys

#Default parameters
INDICATIVE ="F4LEC"
DATE="26/07/68"
UTC="12:00"
MHZ="7.000"
RST ="59"
MODE ="LSB"
TRANSPARENCE =False
SOURCE_IMAGE="F4LEC.jpg"

#default QSL size x=843 , y= 537
WIDTH=843
HEIGHT=537
TEXT_SIZE=25

#Text Color 
BLACK = (0,0,0)
WHITE =(250,250,250)

class InterfaceGraphique(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('QSL F4LEC')
		self.resizable(False, False)		
		self.creeGui() #Cree GUI tkinter
	def creeGui(self):
		""" Crée l'interface utilisateur avec tkinter"""
		#tkinter window
		#self.root.title('QSL F4LEC')
		#self.root.resizable( False, False )	
		
		#Frames
		self.FrameSup=tk.Frame(self, borderwidth=2)	
		self.FrameSup.pack()
		
		self.FrameMed=tk.Frame(self, borderwidth=2)	
		self.FrameMed.pack()		
		
		#Variables 
		self.sIndicative=tk.StringVar(self.FrameSup,value =INDICATIVE)	
		self.sDate=tk.StringVar(self.FrameSup,value =DATE)	
		self.sUtc=tk.StringVar(self.FrameSup,value =UTC)
		self.sMhz=tk.StringVar(self.FrameSup,value =MHZ)
		self.sRst=tk.StringVar(self.FrameSup,value =RST)
		self.sMode=tk.StringVar(self.FrameSup,value =MODE)	
		
		self.sTransparence=tk.BooleanVar(self.FrameSup,value =TRANSPARENCE)
		self.sSource_image=tk.StringVar(self.FrameSup,value =SOURCE_IMAGE)
		
		#data entries
		#Frame Sup
		self.Indicative=tk.Entry(self.FrameSup,textvariable=self.sIndicative,justify='center',bg="white")
		self.Indicative.grid(row=0,column=1)
		
		self.Date=tk.Entry(self.FrameSup,textvariable=self.sDate,justify='center',bg="white")
		self.Date.grid(row=0,column=2)	
		
		self.Utc=tk.Entry(self.FrameSup,textvariable=self.sUtc,justify='center',bg="white")
		self.Utc.grid(row=0,column=3)	
		
		self.Mhz=tk.Entry(self.FrameSup,textvariable=self.sMhz,justify='center',bg="white")
		self.Mhz.grid(row=0,column=4)
		
		self.Rst=tk.Entry(self.FrameSup,textvariable=self.sRst,justify='center',bg="white")
		self.Rst.grid(row=0,column=5)	
		
		self.Mode=tk.Entry(self.FrameSup,textvariable=self.sMode,justify='center',bg="white")
		self.Mode.grid(row=0,column=6)	
		
		#Frame Med
		self.SourceImage=tk.Entry(self.FrameMed,textvariable=self.sSource_image,justify='center',bg="white")
		self.SourceImage.grid(row=0,column=1)	
		
		# Vinculo FocusIn -> método browse_folder
		self.SourceImage.bind("<FocusIn>", self.browse_folder)		
		
		self.Transparence=tk.Entry(self.FrameMed,textvariable=self.sTransparence,justify='center',bg="white")
		self.Transparence.grid(row=0,column=2)	
				
		
	def browse_folder(self, event=None):
		filetypes = (
			('JPEG files', '*.jpg'),
			('PNG files', '*.png'),
			('GIF files', '*.gif'),
			('All image files', ('*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp'))
		)
		
		initial_dir = os.path.dirname(os.path.abspath(__file__))
		
		file_path = filedialog.askopenfilename(
			title='Select image',
			initialdir=initial_dir,
			filetypes=filetypes
		)
		
		if file_path:
			self.sSource_image.set(file_path)
			self.focus_force()  # Devuelve el foco a la ventana
			#self.display_image(file_path)
			
				
						
		
		

if __name__ == "__main__":
  app = InterfaceGraphique() #Instance InterfaceGraphique tkinter
  app.mainloop() #tkinter main loop			
