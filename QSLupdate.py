"""
Antonio Villanueva Segura F4LEC 
Program to edit & print a QSL the input arguments are as follows
STATION DATE UTC MHZ RST MOD


sudo apt-get install python3-pip
sudo apt-get install python3-tk
pip install tk
pip install --upgrade Pillow

pour generer bin
sudo apt-get install patchelf
python3 -m pip install -U nuitka
python3 -m nuitka --standalone --onefile QSLupdate.py
"""
import sys #Arguments
import PIL
from PIL import ImageFont ,Image ,ImageDraw

import tkinter as tk #Gui
from tkinter import ttk
#from tktooltip import ToolTip #infobulles
from tkinter import filedialog

import os
import sys

import time,datetime


#Default parameters
INDICATIVE ="F4LEC"
#DATE="26/07/68"
#UTC="12:00"
DATE=datetime.datetime.today().strftime('%d/%m/%y')
UTC=datetime.datetime.today().strftime('%H:%M')
MHZ="7.000"
RST ="59"
MODE ="LSB"
TRANSPARENCE =False
SOURCE_IMAGE="a.jpg"

#default QSL size x=843 , y= 537
WIDTH=843
HEIGHT=537
TEXT_SIZE=25
MY_TEXT_SIZE=80

#Text Color 
BLACK = (0,0,0)
WHITE =(250,250,250)		  
	
class InterfaceGraphique(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('QSL maker F4LEC')
		self.resizable(False, False)	
		self.dialog_open = False	
		
		#QSL class instance
		self.qsl =QSL()
		
		#GUI tkinter
		self.creeGui() 
		
	def creeGui(self):
		""" Crée l'interface utilisateur avec tkinter"""
		
		#Frames	,Frames to place the different objects	
		self.FrameMyStation=tk.Frame(self, borderwidth=2)	
		self.FrameMyStation.pack()
		
		self.FrameSup=tk.Frame(self, borderwidth=2)	
		self.FrameSup.pack()
		
		self.FrameMed=tk.Frame(self, borderwidth=2)	
		self.FrameMed.pack()		
		
		self.FrameButtons=tk.Frame(self, borderwidth=2)	
		self.FrameButtons.pack()			
		
		#Variables 		
		self.sMyIndicative=tk.StringVar(self.FrameMyStation,value =INDICATIVE)
		self.iPosX=	tk.IntVar(self.FrameMyStation,value =1)	
		self.iPosY=	tk.IntVar(self.FrameMyStation,value =1)	
		self.iSizeText=	tk.IntVar(self.FrameMyStation,value =MY_TEXT_SIZE)	
				
		self.sIndicative=tk.StringVar(self.FrameSup,value =INDICATIVE)	
		self.sDate=tk.StringVar(self.FrameSup,value =DATE)	
		self.sUtc=tk.StringVar(self.FrameSup,value =UTC)
		self.sMhz=tk.StringVar(self.FrameSup,value =MHZ)
		self.sRst=tk.StringVar(self.FrameSup,value =RST)
		self.sMode=tk.StringVar(self.FrameSup,value =MODE)	
		
		self.bTransparence=tk.BooleanVar(self.FrameSup,value =TRANSPARENCE)
		self.sSource_image=tk.StringVar(self.FrameSup,value =SOURCE_IMAGE)
		
		#Frame FrameMyStation data entries		
		labelMyCallSign = tk.Label(self.FrameMyStation, text="My callsign")
		labelMyCallSign.grid(row=0, column=1, sticky="e", padx=5, pady=5)
		
		self.MyIndicative=tk.Entry(self.FrameMyStation,textvariable=self.sMyIndicative,justify='center',bg="yellow")
		self.MyIndicative.grid(row=0,column=2)		
		
		labelX = tk.Label(self.FrameMyStation, text="X")
		labelX.grid(row=0, column=3, sticky="e", padx=5, pady=5)		
		
		self.MyPosX=tk.Entry(self.FrameMyStation,textvariable=self.iPosX,justify='center',bg="yellow")
		self.MyPosX.grid(row=0,column=4)	
		
		
		labelY = tk.Label(self.FrameMyStation, text="Y")
		labelY.grid(row=0, column=5, sticky="e", padx=5, pady=5)
		
		self.MyPosY=tk.Entry(self.FrameMyStation,textvariable=self.iPosY,justify='center',bg="yellow")
		self.MyPosY.grid(row=0,column=6)	
		
		labelY = tk.Label(self.FrameMyStation, text="SIZE")
		labelY.grid(row=0, column=7, sticky="e", padx=5, pady=5)
		
		self.MySizeText=tk.Entry(self.FrameMyStation,textvariable=self.iSizeText,justify='center',bg="yellow")
		self.MySizeText.grid(row=0,column=8)					
		
		
		#Frame Sup Labels 
		labelIndicative = tk.Label(self.FrameSup, text="indicative", width=25, anchor="center")
		labelIndicative.grid(row=0, column=0, sticky="e", padx=5, pady=5)
		
		labelDate = tk.Label(self.FrameSup, text="Date", width=25, anchor="center")
		labelDate.grid(row=0, column=1, sticky="e", padx=5, pady=5)
		
		labelUtc = tk.Label(self.FrameSup, text="UTC", width=25, anchor="center")
		labelUtc.grid(row=0, column=2, sticky="e", padx=5, pady=5)
		
		labelMhz = tk.Label(self.FrameSup, text="Mhz", width=25, anchor="center")
		labelMhz.grid(row=0, column=3, sticky="e", padx=5, pady=5)
		
		labelRst = tk.Label(self.FrameSup, text="RST", width=25, anchor="center")
		labelRst.grid(row=0, column=4, sticky="e", padx=5, pady=5)
		
		labelMode = tk.Label(self.FrameSup, text="Mode", width=25, anchor="center")
		labelMode.grid(row=0, column=5, sticky="e", padx=5, pady=5)		
		
		
		#FrameSup Entries		
		self.Indicative=tk.Entry(self.FrameSup,textvariable=self.sIndicative,justify='center',bg="white")
		self.Indicative.grid(row=1,column=0)		
		
		self.Date=tk.Entry(self.FrameSup,textvariable=self.sDate,justify='center',bg="white")
		self.Date.grid(row=1,column=1)	
		
		self.Utc=tk.Entry(self.FrameSup,textvariable=self.sUtc,justify='center',bg="white")
		self.Utc.grid(row=1,column=2)	
		
		self.Mhz=tk.Entry(self.FrameSup,textvariable=self.sMhz,justify='center',bg="white")
		self.Mhz.grid(row=1,column=3)
		
		self.Rst=tk.Entry(self.FrameSup,textvariable=self.sRst,justify='center',bg="white")
		self.Rst.grid(row=1,column=4)	
		
		self.Mode=tk.Entry(self.FrameSup,textvariable=self.sMode,justify='center',bg="white")
		self.Mode.grid(row=1,column=5)	
		
		#Frame Med
		
		labelSourceImage = tk.Label(self.FrameMed, text="Source Base Image", width=25, anchor="center")
		labelSourceImage.grid(row=0, column=1, sticky="e", padx=5, pady=5)	
		
		self.SourceImage=tk.Entry(self.FrameMed,textvariable=self.sSource_image,justify='center',bg="white")
		self.SourceImage.grid(row=1,column=1)	
		
		# Vinculo  -> método browse_folder
		#self.SourceImage.bind("<FocusIn>", self.browser_folder)		
		self.SourceImage.bind("<Button-1>", self.browser_folder)	
		
		labelTransparence = tk.Label(self.FrameMed, text="Transparence", width=25, anchor="center")
		labelTransparence.grid(row=0, column=2, sticky="e", padx=5, pady=5)
		
		self.TransparenceButton=tk.Checkbutton(self.FrameMed, text='Transparence',variable=self.bTransparence)
		self.TransparenceButton.grid(row=1,column=2)
		
		#Frame Buttons	 Button to create the QSL
		self.CreateQSL=tk.Button(self.FrameButtons,text="Create", bg="red",
		command=self.CreateQSL)	
		self.CreateQSL.grid(row=0 ,column=2)
		
	def CreateQSL(self):
		""" Function to configure the QSL class variables retrieved from the graphical interface """
		self.qsl.set_mystation (self.sMyIndicative.get())
		self.qsl.set_Xpos (self.iPosX.get())
		self.qsl.set_Ypos (self.iPosY.get())	
		self.qsl.set_SizeText (self.iSizeText.get())			
		
		self.qsl.set_station (self.sIndicative.get())
		self.qsl.set_date (self.sDate.get())
		self.qsl.set_utc (self.sUtc.get())
		self.qsl.set_mhz (self.sMhz.get())
		self.qsl.set_rst (self.sRst.get())
		self.qsl.set_mode (self.sMode.get())
		self.qsl.set_station (self.sIndicative.get())
		self.qsl.set_transparence(self.bTransparence.get())
		self.qsl.set_source_image (self.sSource_image.get() )												
		self.qsl.run()
				
	def browser_folder(self, event=None):
		""" Function to browse and select image files """
		if self.dialog_open:
			return
		filetypes = (
			('All image files', ('*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp')),
			('JPEG files', '*.jpg'),
			('PNG files', '*.png'),
			('GIF files', '*.gif')
		)
		
		initial_dir = os.path.dirname(sys.modules["__main__"].__file__)
		#initial_dir = os.path.dirname(os.path.abspath(__file__))
		
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
	""" This class is the heart of the creation of the QSL card """
	def __init__(self):		
		self.mystation=None
		self.myXpos=None
		self.myYpos=None
		self.MySizeText=None
		
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

	#setters  To configure the different variables
	def set_mystation(self,data):
		self.mystation=data
		
	def set_Xpos(self,data):
		self.myXpos=data	
		
	def set_Ypos(self,data):
		self.myYpos=data	
		
	def set_SizeText(self,data):
		self.MySizeText=data					
		
	def set_station(self,data):
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
		
	def set_transparence (self,data):
		self.transparence =data		
		
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
		"""Load text fonts with size"""
		
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
		"""Create the box with the QSL contact information """
		x0 = 0
		x1 = x
		y0 = y - (y / 8)
		y1 = y

		# Create a new image with alpha channel
		if transparent:
			overlay = Image.new('RGBA', (x, y), (255, 255, 255, 0))
			d = ImageDraw.Draw(overlay)
		else:
			d = draw

		# Draw the rectangle
		d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, 0) if transparent else (255, 255, 255, 255), outline=color, width=2)

		# Draw six vertical lines inside the rectangle
		num_vertical_lines = 6
		line_spacing = (x1 - x0) / (num_vertical_lines + 1)

		for i in range(1, num_vertical_lines + 1):
			x_line = x0 + i * line_spacing
			d.line([(x_line, y0), (x_line, y1)], fill=color, width=1)

		# Draw a horizontal line inside the rectangle
		horizontal_y = (y0 + y1) / 2
		d.line([(x0, horizontal_y), (x1, horizontal_y)], fill=color, width=1)

		# If transparent, merge the overlay with the original image
		if transparent:
			draw.bitmap((0, 0), overlay)

	def write_user_data(self,draw,myX,myY,mySizeText,color=BLACK):
		""" Write the text data in the QSL """
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
		

		#Maximum size control for the position and size of my text 
		if myX>self.WIDTH:
			myX=( self.WIDTH - mySizeText*3 )
		
		if myY >self.HEIGHT:
			myY= ( self.HEIGHT -mySizeText  -10 )
		
		#Write my station's data in the QSL
		self.font=self.load_font(mySizeText)
		draw.text((myX, myY), self.mystation ,color,font=self.font)		
		

	def resize_image(self,x,y,img):
		""" Resize image"""
		print('Debug Org Image Size x : ',x,', y:',y) #Analyze the size of the out QSL  p.e x=843 , y= 537
		if (x!=self.WIDTH or y!=self.HEIGHT) :	

			img = img.resize((self.WIDTH, self.HEIGHT), Image.Resampling.BICUBIC)
			#Get size of image
			x, y = img.size
			print('Debug New Image Size x : ',x,', y:',y) #Analyze the size of the out QSL  p.e x=843 , y= 537
		return img
	
	def run (self):
		""" Main function of the QSL class """

		#Load Text Font
		self.font=self.load_font()

		#Read photo image
		self.img=self.read_image (self.source_image) 

		#Get size of image
		x, y = self.img.size

		#Resize image,  default QSL size x=843 , y= 537
		self.img=self.resize_image(x,y,self.img)

		# Creates objtect draw   
		self.draw = ImageDraw.Draw(self.img)

		#Create the bottom square containing contact data
		self.creeCadre(self.WIDTH ,self.HEIGHT ,self.draw,"black",self.transparence)


		#Write User , contact data QSL
		self.write_user_data (self.draw,self.myXpos,self.myYpos,self.MySizeText)

		#Drawing in img
		draw = ImageDraw.Draw(self.img)

		#Show image
		self.img.show()

		# Save image with extension 
		ext= (self.source_image) .split(".")[-1]
		self.img.save( self.station+"."+ext)
	
if __name__ == "__main__":
  app = InterfaceGraphique() #Instance InterfaceGraphique tkinter
  app.mainloop() #tkinter main loop			
