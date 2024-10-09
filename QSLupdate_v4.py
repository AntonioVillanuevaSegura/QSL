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
		self.dialog_open = False	
		
		self.qsl =QSL()
		self.creeGui() #Cree GUI tkinter
	def creeGui(self):
		""" Crée l'interface utilisateur avec tkinter"""
		
		#Frames
		self.FrameSup=tk.Frame(self, borderwidth=2)	
		self.FrameSup.pack()
		
		self.FrameMed=tk.Frame(self, borderwidth=2)	
		self.FrameMed.pack()		
		
		self.FrameButtons=tk.Frame(self, borderwidth=2)	
		self.FrameButtons.pack()			
		
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
		
		# Vinculo  -> método browse_folder
		#self.SourceImage.bind("<FocusIn>", self.browser_folder)		
		self.SourceImage.bind("<Button-1>", self.browser_folder)	
		
		self.Transparence=tk.Entry(self.FrameMed,textvariable=self.sTransparence,justify='center',bg="white")
		self.Transparence.grid(row=0,column=2)
		
		#Frame Buttons	
		
		self.CreateQSL=tk.Button(self.FrameButtons,text="Create", bg="red",
		command=self.CreateQSL)	
		self.CreateQSL.grid(row=0 ,column=1)
		
	def CreateQSL(self):
		
		self.qsl.set_station (self.sIndicative.get())
		self.qsl.set_date (self.sDate.get())
		self.qsl.set_utc (self.sUtc.get())
		self.qsl.set_mhz (self.sMhz.get())
		self.qsl.set_rst (self.sRst.get())
		self.qsl.set_mode (self.sMode.get())
		self.qsl.set_station (self.sIndicative.get())
		self.qsl.set_source_image (self.sSource_image.get() )												
		self.qsl.run()
				
	def browser_folder(self, event=None):
		if self.dialog_open:
			return
		filetypes = (
			('JPEG files', '*.jpg'),
			('PNG files', '*.png'),
			('GIF files', '*.gif'),
			('All image files', ('*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp'))
		)
		
		initial_dir = os.path.dirname(os.path.abspath(__file__))
		
		try:
			file_path = filedialog.askopenfilename(
				title='Select Base QSL image',
				initialdir=initial_dir,
				filetypes=filetypes,
				parent=self
			)
		finally:
			self.dialog_open = False			
			self.focus_force()
			self.lift()

		if file_path:
			self.sSource_image.set(file_path)
			self.SourceImage.update()
			print(f"Selected file: {file_path}")
		else:
			print ("Cancel")
				
class QSL():
	def __init__(self):		
		self.station =None
		self.date=None
		self.utc=None
		self.mhz=None
		self.rst=None
		self.mode=None
		self.transparence=False
		self.source_image=SOURCE_IMAGE
		self.image=None
		self.draw=None
		self.font=None
		
		#default QSL size x=843 , y= 537
		self.WIDTH=843
		self.HEIGHT=537
		self.TEXT_SIZE=25
		
	def set_station(self,data):
		print ("DEBUG ----------> ",data)
		self.station=data
		
	def set_date (self,data):
		self.date=data	
		
	def set_utc (self,data):
		self.utc=data
		
	def set_mhz (self,data):
		self.mhz=data	
		
	def set_rst (self,data):
		self.rst=data	
		
	def set_mode (self,data):
		self.mode=data											
	 
	def set_source_image (self,data):
		self.source_image =data
		
	def read_image(self,fichier):
		"""Read base image  """
		print ("Debug base file image :" ,fichier)
		#Image default Source
		imageFile = fichier

		#Try open image
		try:
			img=Image.open(imageFile)
		except IOError:
			print("Impossible d'ouvrir l'image .arrière-plan blanc par défaut")
			img = Image.new("RGB", (width, height), "white")
		
		return img
		
	def load_font(self,taille=TEXT_SIZE):
		"""text font 
		/usr/share/fonts/truetype/freefont/
		FreeMonoBoldOblique.ttf  FreeSansBoldOblique.ttf  FreeSerifBoldItalic.ttf
		FreeMonoBold.ttf         FreeSansBold.ttf         FreeSerifBold.ttf
		FreeMonoOblique.ttf      FreeSansOblique.ttf      FreeSerifItalic.ttf
		FreeMono.ttf             FreeSans.ttf             FreeSerif.ttf
		"""
		
		fonts = [
			"/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",
			"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
			"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
			"/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"
		]

		for font in fonts:
			try:
				return ImageFont.truetype(font, taille, encoding="unic")
			except IOError:
				continue

		print("Aucune police TrueType trouvée. Utilisation de la police par défaut.")
		return ImageFont.load_default()

	def creeCadre(self,x, y, draw,color="black", transparent=False):
		x0 = 0
		x1 = x
		y0 = y - (y / 8)
		y1 = y

		# Crear una nueva imagen con canal alfa
		if transparent:
			overlay = Image.new('RGBA', (x, y), (255, 255, 255, 0))
			d = ImageDraw.Draw(overlay)
		else:
			d = draw

		# Dibuja el rectángulo
		d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, 0) if transparent else (255, 255, 255, 255), outline=color, width=2)

		# Dibuja seis líneas verticales dentro del rectángulo
		num_vertical_lines = 6
		line_spacing = (x1 - x0) / (num_vertical_lines + 1)

		for i in range(1, num_vertical_lines + 1):
			x_line = x0 + i * line_spacing
			d.line([(x_line, y0), (x_line, y1)], fill=color, width=1)

		# Dibuja una línea horizontal dentro del rectángulo
		horizontal_y = (y0 + y1) / 2
		d.line([(x0, horizontal_y), (x1, horizontal_y)], fill=color, width=1)

		# Si es transparente, combina la superposición con la imagen original
		if transparent:
			draw.bitmap((0, 0), overlay)

	def write_user_data(self,draw,color=BLACK):
		#Line Y of the text level
		x=self.WIDTH #default
		y=self.HEIGHT #default
		y_text=y-(y/8)+(TEXT_SIZE/2)-4
		
		#Draw STATION 
		draw.text((12, y_text), "STATION " ,color,font=self.font)

		#Draw DATE
		draw.text((122+30, y_text), "DATE" ,color,font=self.font)

		#Draw HOUR
		draw.text((260, y_text), "UTC" ,color,font=self.font)

		#Draw Mhz
		draw.text((380, y_text), "MHZ" ,color,font=self.font)

		#Draw RST
		draw.text((520, y_text), "RST" ,color,font=self.font)

		#Draw MODE
		draw.text((630, y_text), "MODE" ,color,font=self.font)

		#Draw QSL 
		draw.text((750, y_text), "QSL" ,color,font=self.font)


		y_text = y_text+TEXT_SIZE
		#Draw STATION 
		draw.text((12, y_text), self.station ,color,font=self.font)

		#Draw DATE
		draw.text((122, y_text), self.date ,color,font=self.font)

		#Draw HOUR
		draw.text((260, y_text), self.utc ,color,font=self.font)

		#Draw Mhz
		draw.text((380, y_text), self.mhz ,color,font=self.font)

		#Draw RST
		draw.text((520, y_text), self.rst ,color,font=self.font)

		#Draw MODE
		draw.text((630, y_text), self.mode ,color,font=self.font)

	def resize_image(self,x,y,img):
		#Resize image
		print('Debug Org Image Size x : ',x,', y:',y) #Analyze the size of the out QSL  p.e x=843 , y= 537
		if (x!=self.WIDTH or y!=self.HEIGHT) :	
			img = img.resize((self.WIDTH, self.HEIGHT), Image.Resampling.BICUBIC)
			#Get size of image
			x, y = img.size
			print('Debug New Image Size x : ',x,', y:',y) #Analyze the size of the out QSL  p.e x=843 , y= 537
		return img
	
	def run (self):
		#Obtains arguments from the program execution
		#read_arguments() 
		
		print ("Create QSL")
		print (" sta :" ,self.station)
		#Text Font
		self.font=self.load_font()

		self.img=self.read_image (self.source_image) #Read base image

		#Get size of image
		x, y = self.img.size

		self.img=self.resize_image(x,y,self.img)	#Resize image

		# Creates objtect draw   
		self.draw = ImageDraw.Draw(self.img)

		#Cadre
		self.creeCadre(self.WIDTH ,self.HEIGHT ,self.draw,"black",self.transparence)

		#User data QSL
		self.write_user_data (self.draw)

		#Drawing in img
		draw = ImageDraw.Draw(self.img)

		#img = ImageDraw.Draw(img)

		#Show image
		self.img.show()

		# Save image
		self.img.save( "QSL_output.jpg")
	
if __name__ == "__main__":
  app = InterfaceGraphique() #Instance InterfaceGraphique tkinter
  app.mainloop() #tkinter main loop			
