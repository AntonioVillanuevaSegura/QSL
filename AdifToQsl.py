"""
Antonio Villanueva Segura F4LEC 
version to read adif file and create QSLs

NOTE The adif format has a field called FREQ but the adif used by eqsl does not use it !!!!


pip install adif-io

Référence ADIF
https://adif.org.uk/
https://www.adif.org.uk/310/ADIF_310.htm

adif validator
https://www.rickmurphy.net/adifvalidator.html

sudo apt-get install python3-pip
sudo apt-get install python3-tk
pip install tk
pip install --upgrade Pillow

pour generer bin
sudo apt-get install patchelf
python3 -m pip install -U nuitka
python3 -m nuitka --standalone --onefile --enable-plugin=tk-inter QSLupdate.py
"""
import sys #Arguments
import PIL
from PIL import ImageFont ,Image ,ImageDraw

import tkinter as tk #Gui
from tkinter import ttk
#from tktooltip import ToolTip #infobulles
from tkinter import filedialog
from tkinter import colorchooser

import os
import sys

import time,datetime


import re

#Default parameters
VERSION_SOFT= "3.0 Adif to QSL"
MY_CALL ="F4LEC"
#DATE=datetime.datetime.today().strftime('%d/%m/%y')
DATE=datetime.datetime.today().strftime('%Y/%m/%d')

UTC=datetime.datetime.today().strftime('%H:%M')
BAND="40m"
MHZ="7.000"
RST ="59"
MODE ="SSB"
SUBMODE="LSB"
GRIDSQUARE="JN33qr" #user grid square
QSLMSG="TNX QSO 73s"
TRANSPARENCE =False
SOURCE_IMAGE=""

#GUI
#TEXT_WIDTH =20

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
		#self.geometry("1000x500")
		self.title('QSL maker F4LEC')
		self.resizable(False, False)	
		self.dialog_open = False	
		
		#QSL class instance
		#self.qsl =QSL()
		
		#Adif class instance
		self.adif =AdifExtract()		

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
		self.sMY_CALL=tk.StringVar(self.FrameMyStation,value =MY_CALL)
		self.sQSLMSG=tk.StringVar(self.FrameSup,value =QSLMSG)
		self.iPosX=	tk.IntVar(self.FrameMyStation,value =1)	
		self.iPosY=	tk.IntVar(self.FrameMyStation,value =1)	
		self.iSizeText=	tk.IntVar(self.FrameMyStation,value =MY_TEXT_SIZE)

		self.bTransparence=tk.BooleanVar(self.FrameSup,value =TRANSPARENCE)
		self.sSource_image=tk.StringVar(self.FrameSup,value =SOURCE_IMAGE)
		self.sSource_adif=tk.StringVar(self.FrameSup,value =None)
		self.sTextColor=tk.StringVar(self.FrameMed,value="#000000" )
		self.sFrameColor=tk.StringVar(self.FrameMed,value="#000000" )
		
		#Frame FrameMyStation data entries	
			
		labelMyCallSign = tk.Label(self.FrameMyStation, text="MY CALLSIGN",anchor="center",width=15)
		labelMyCallSign.grid(row=0, column=0,padx=4, pady=4)
		
		self.MY_CALL=tk.Entry(self.FrameMyStation,textvariable=self.sMY_CALL,justify='center',bg="yellow",width=20)
		self.MY_CALL.grid(row=1,column=0)		
		
		
		labelX = tk.Label(self.FrameMyStation, text="X",anchor="center",width=1)
		labelX.grid(row=0, column=1, padx=4, pady=4)		
		
		self.MyPosX=tk.Entry(self.FrameMyStation,textvariable=self.iPosX,justify='center',bg="yellow",width=5)
		self.MyPosX.grid(row=1,column=1)	
		
		
		labelY = tk.Label(self.FrameMyStation, text="Y",anchor="center",width=1)
		labelY.grid(row=0, column=2, padx=4, pady=4)
		
		self.MyPosY=tk.Entry(self.FrameMyStation,textvariable=self.iPosY,justify='center',bg="yellow",width=5)
		self.MyPosY.grid(row=1,column=2)	
		
		
		labelSize = tk.Label(self.FrameMyStation, text="SIZE",anchor="center",width=5)
		labelSize.grid(row=0, column=3, padx=4, pady=4)
		
		self.MySizeText=tk.Entry(self.FrameMyStation,textvariable=self.iSizeText,justify='center',bg="yellow",width=5)
		self.MySizeText.grid(row=1,column=3)
		
		
		labelQSLMSG = tk.Label(self.FrameMyStation, text="QSLMSG",anchor="center",width=5)
		labelQSLMSG.grid(row=2, column=1,sticky="we", padx=4, pady=4)
		
		self.QSLMSG=tk.Entry(self.FrameMyStation,textvariable=self.sQSLMSG,justify='center',bg="yellow",width=50)
		self.QSLMSG.grid(row=3,column=0,columnspan=4)		
			
		
		#Frame Med Source Image Colors  ...
		
		#Source Base Image
		
		labelSourceImage = tk.Label(self.FrameSup, text="Source Base Image", anchor="center")
		labelSourceImage.grid(row=0, column=1, padx=4, pady=4)	
		
		self.SourceImage=tk.Entry(self.FrameSup,textvariable=self.sSource_image,justify='center',bg="white")
		self.SourceImage.grid(row=1,column=1)	
		
		#self.SourceImage.bind("<Button-1>", self.browser_folder)
		self.SourceImage.bind("<Button-1>", lambda event, arg="image": self.browser_folder(event, arg))
		
		#Source Adif
		labelSourceAdif = tk.Label(self.FrameSup, text="Source Adif", anchor="center")
		labelSourceAdif.grid(row=0, column=2, padx=4, pady=4)	
		
		self.SourceAdif=tk.Entry(self.FrameSup,textvariable=self.sSource_adif,justify='center',bg="white")
		self.SourceAdif.grid(row=1,column=2)	
				
		#self.SourceAdif.bind("<Button-1>", self.browser_folder)		
		self.SourceAdif.bind("<Button-1>", lambda event, arg="adif": self.browser_folder(event, arg))		
		
	
		
		labelTransparence = tk.Label(self.FrameMed, text="Transparence", anchor="center")
		labelTransparence.grid(row=0, column=2, padx=4, pady=4)
				
		self.TransparenceButton=tk.Checkbutton(self.FrameMed, text='Transparence',variable=self.bTransparence)
		self.TransparenceButton.grid(row=1,column=2)
		
		labelcolorText = tk.Label(self.FrameMed, text="Text Color", anchor="center")
		labelcolorText.grid(row=0, column=3, padx=4, pady=4)
		
		self.TextColor = tk.Button(self.FrameMed, text="Text Color", command=self.choose_text_color)
		self.TextColor.grid(row=1 ,column=3)
		
		labelcolorFrame = tk.Label(self.FrameMed, text="Frame Color", anchor="center")
		labelcolorFrame.grid(row=0, column=4, padx=4, pady=4)
		
		self.FrameColor = tk.Button(self.FrameMed, text="Frame Color", command=self.choose_frame_color)
		self.FrameColor.grid(row=1 ,column=4)		
		
		
		#Frame Buttons	 Button to create the QSL
		self.Create=tk.Button(self.FrameButtons,text="Create", bg="red",
		command=self.Create)	
		self.Create.grid(row=0 ,column=2)
		

	def choose_text_color(self):
		color = colorchooser.askcolor(title="Choose color")
		if color[1]:
			#self.sTextColor = color[1]
			self.sTextColor.set(color[1])
			
	def choose_frame_color(self):
		color = colorchooser.askcolor(title="Choose color")
		if color[1]:
			#self.sFrameColor = color[1]
			self.sFrameColor.set(color[1])
						
	def Create(self):
		""" Function to configure& create the QSL & Adif class variables retrieved from the graphical interface """
		
		if self.sMY_CALL.get()=="":
			print ("Error :My CALL is empty !")
			return
		
		
		qsl_data={
				'MY_CALL': self.sMY_CALL.get(),
				'X_MY_CALL':self.iPosX.get(),
				'Y_MY_CALL':self.iPosY.get(),
				'SIZE_MY_CALL':self.iSizeText.get(),
				'QSLMESSAGE':self.sQSLMSG.get(),	
				'CALL':None,
				'QSO_DATE':None,
				'TIME_ON':None,
				'BAND': None,				
				'FREQ':None,
				'RST_SEND':None,
				'MODE':None,
				'SUBMODE':None,	
				'SOURCE_IMAGE':self.sSource_image.get(),
				'TRANSPARENCE':self.bTransparence.get(),
				'FRAME_COLOR':self.sFrameColor.get(),
				'TEXT_COLOR':self.sTextColor.get(),
				'SOURCE_IMAGE':self.sSource_image.get()			
			}
		self.adif.setup_adif_file(self.sSource_adif.get())
		self.adif.setup_qsl_data (qsl_data)
		self.adif.run()
	
	def browser_folder(self, event, extra_arg):
		""" Select an image file that will be the basis of the QSL """
		if self.dialog_open:
			return
		
		if extra_arg=="image":	
			filetypes = (
				('All image files', ('*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp')),
				('JPEG files', '*.jpg'),
				('PNG files', '*.png'),
				('GIF files', '*.gif')
			)
		else:
			filetypes = (
				('All files', '*.*'),
				('Adif files', '*.adif'),
				('Text files', '*.txt'),
				('CSV files', '*.csv')
			)
		
		initial_dir = os.path.dirname(sys.modules["__main__"].__file__)
		#initial_dir = os.path.dirname(os.path.abspath(__file__))
		
		try:
			file_path = filedialog.askopenfilename(
				title='Select '+extra_arg+' file',
				initialdir=initial_dir,
				filetypes=filetypes,
				multiple=False,
				parent=self
			)
		finally:
			self.dialog_open = False			
			self.focus_force()
			self.lift()

		if file_path:
			if extra_arg=="image":
				self.sSource_image.set(file_path)
				self.SourceImage.update()
			else:
				self.sSource_adif.set(file_path)
				self.SourceAdif.update()
			print(f"Selected file: {file_path}")
		else:
			print ("Cancel")
		
class AdifExtract():
		def __init__(self):	

			self.qsl =QSL()	#QSL class instance
			self.AdifFILE=None #Adif file to read
			self.AdifTXT=None #Adif file txt
			#Data retrieved from tkinter GUI
			self.qsl_data={
				'MY_CALL': None,
				'X_MY_CALL':None,
				'Y_MY_CALL':None,
				'SIZE_MY_CALL':None,
				'QSLMESSAGE':None,	
				'CALL':None,
				'QSO_DATE':None,
				'TIME_ON':None,
				'BAND': None,				
				'FREQ':None,
				'RST_SEND':None,
				'MODE':None,
				'SUBMODE':None,					
				'SOURCE_IMAGE':None,
				'TRANSPARENCE':None,
				'FRAME_COLOR':None,
				'TEXT_COLOR':None,
				'SOURCE_IMAGE':None				
			}
			
			#Data recovered by reading the adif file line by line
			self.contact_model = {
				'CALL': None,
				'EMAIL': None,
				'QSO_DATE': None,
				'TIME_ON': None,
				'BAND': None,
				'FREQ': None,
				'MODE': None,
				'SUBMODE': None,
				'RST_SENT': None,
				'RST_RCVD': None,
				'QSL_SENT': None,
				'QSL_SENT_VIA': None,
				'QSLMSG': None,
				'APP_EQSL_AG': None,
				'GRIDSQUARE': None,
				'EQSL_QSL_RCVD': None,
				'EQSL_QSLRDATE': None
			}

		def clear_dictionary (self,dictionary):
			""" clears the values ​​from a dictionary p.e self.contact_model"""
			for key in dictionary:
				dictionary[key]='None'
				
		def setup_adif_file(self,data):
			""" Adif file to open"""
			self.AdifFILE=data
			
		def setup_qsl_data(self,data):
			"""Updates self.contact_model with the remote dictionary """
			self.qsl_data=data
						
		def setup_contact_data(self,data):
			"""Updates self.contact_model with the remote dictionary """
			self.contact_model=data
			
		def copy_dict_to_contact_model (self, data):
			""" Copy only common keys to dictionaries"""
			#clear the values ​​of the self.contact_model
			self.clear_dictionary (self.contact_model)
			
			copy = {k: data[k] for k in self.contact_model.keys() & data.keys()}
			return copy
		
		def update_qsl_data(self,data):
			""" Updates qsl_data with the common data in the data dictionary """
			
			for key, value in data.items():
				
				if key in self.qsl_data:
					self.qsl_data[key]=value
							
		def open_adif(self):
			""" open & read AdifFILE in AdifTXT"""

			with open(self.AdifFILE, 'r', encoding='iso-8859-1') as archivo:
			#with open(self.AdifFILE, 'r', encoding='utf-8') as archivo:
			#with open(self.AdifFILE, 'r') as archivo:
				self.AdifTXT = archivo.read()
		
		def read_lines(self):
			""" Read lines in AdifTXT , updates self.contact_model"""
			
			#read line by line Adif txt , create a dictionary from each line 
			for line in self.AdifTXT.split('<EOR>'):

				#Get Dictionnaryfrom Adif line
				adif_dict=self.dict_from_adif_line(line) 
				
				#Copy  only key1=key2 is the same
				new_dict = self.copy_dict_to_contact_model(adif_dict)
				self.setup_contact_data(new_dict)

				#Copy self.contact_model to self.qsl_data
				self.update_qsl_data(self.contact_model)
				
				#Set data to QSL class 
				print ("DEBUG C :",self.contact_model)				
				print ("DEBUG Q :",self.qsl_data)
				self.qsl.setup_qsl_data(self.qsl_data)
				
				#Create QSL
				self.qsl.run()

					
		def dict_from_adif_line(self,line):
			"""Create a dictionary with keys and values from adif"""
			pattern = r'<(\w+)(?::\d+:?\w?)?>(.*?)(?=<|$)'	
			#Create the dictionary
			adif_dict = dict(re.findall(pattern, line))	
			
			#Remove EOR
			adif_dict.pop('EOR', None)	
			return adif_dict
			
		def run (self):
			""" main """
			
			#Open Adif Files
			self.open_adif ()
			#Read lines and create QSL
			self.read_lines()				
		
class QSL():
	""" This class is the heart of the creation of the QSL card """
	def __init__(self):	

		self.image=None
		self.draw=None
		self.font=None

		qsl_data={
			'MY_CALL': None,
			'X_MY_CALL':None,
			'Y_MY_CALL':None,
			'SIZE_MY_CALL':None,
			'QSLMESSAGE':None,	
			'CALL':None,
			'QSO_DATE':None,
			'TIME_ON':None,
			'FREQ':None,
			'RST_SEND':None,
			'MODE':None,
			'SUBMODE':None,			
			'SOURCE_IMAGE':None,
			'TRANSPARENCE':None,
			'FRAME_COLOR':None,
			'TEXT_COLOR':None,
			'SOURCE_IMAGE':None
		}
		
		self.color_frame=None
		self.color_text=None
		
		#default QSL size x=843 , y= 537
		self.WIDTH=843
		self.HEIGHT=537
		self.TEXT_SIZE=25

	#setters  To configure the different variables

	def setup_qsl_data(self,data):
		"""Updates the local dictionary with the remote dictionary """
		self.qsl_data=data
		#print (self.qsl_data)	
			
	def read_image(self,fichier):
		"""Read base image  """
		#print ("DEBUG base file image :" ,fichier)
		#Image default Source
		imageFile = fichier
		#No image selected as background
		if (fichier==""):
			img = Image.new("RGB", (self.WIDTH, self.HEIGHT), "white")
			print ("You have not selected any image, I use white image by default")
			return img

		#Try open image
		try:
			img=Image.open(imageFile)
		except IOError:
			print("Impossible d'ouvrir l'image .arrière-plan blanc par défaut")
			img = Image.new("RGB", (self.WIDTH, self.HEIGHT), "white")
		
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
		y_text=y-(y/8)+(TEXT_SIZE/2)-6
		
		#Draw MSG
		draw.text((5, y_text-40), self.qsl_data ['QSLMESSAGE'],color,font=self.font)
		
		#Draw STATION 
		draw.text((12, y_text), "STATION " ,color,font=self.font)

		#Draw DATE
		draw.text((122+30, y_text), "DATE" ,color,font=self.font)

		#Draw HOUR
		draw.text((272, y_text), "UTC" ,color,font=self.font)

		#Draw Mhz
		draw.text((395, y_text), "MHZ" ,color,font=self.font)

		#Draw RST
		draw.text((520, y_text), "RST" ,color,font=self.font)

		#Draw MODE
		draw.text((630, y_text), "MODE" ,color,font=self.font)

		#Draw SUBMODE 
		draw.text((750, y_text), "SUBMODE" ,color,font=self.font)

		y_text = y_text+TEXT_SIZE+6
		#Draw STATION 
		if self.qsl_data ['CALL']!=None:		
			draw.text((12, y_text), self.qsl_data ['CALL'] ,color,font=self.font)

		#Draw DATE
		if self.qsl_data ['QSO_DATE']!=None:			
			draw.text((122, y_text), self.qsl_data ['QSO_DATE'] ,color,font=self.font)

		#Draw HOUR
		if self.qsl_data ['TIME_ON']!=None:		
			draw.text((260, y_text), self.qsl_data ['TIME_ON'] ,color,font=self.font)

		#Draw Mhz
		if self.qsl_data ['FREQ']!=None:
			draw.text((380, y_text), self.qsl_data ['FREQ'] ,color,font=self.font)

		#Draw RST
		if self.qsl_data ['RST_SEND']!=None:		
			draw.text((520, y_text), self.qsl_data ['RST_SENT'] ,color,font=self.font)

		#Draw MODE
		if self.qsl_data ['MODE']!=None:		
			draw.text((630, y_text), self.qsl_data ['MODE'] ,color,font=self.font)
		
		#Draw SUBMODE
		if self.qsl_data ['SUBMODE']!=None:		
			draw.text((750, y_text), self.qsl_data ['SUBMODE'] ,color,font=self.font)		
		
		#Write message if it exists

		#Maximum size control for the position and size of my text 
		if myX>self.WIDTH:
			myX=( self.WIDTH - mySizeText*3 )
		
		if myY >self.HEIGHT:
			myY= ( self.HEIGHT -mySizeText  -10 )
		
		#Write my station's data in the QSL
		self.font=self.load_font(mySizeText)
		draw.text((myX, myY), self.qsl_data['MY_CALL'] ,color,font=self.font)		
		
	def resize_image(self,x,y,img):
		""" Resize image"""
		#print('Debug Org Image Size x : ',x,', y:',y) #Analyze the size of the out QSL  p.e x=843 , y= 537
		if (x!=self.WIDTH or y!=self.HEIGHT) :	

			img = img.resize((self.WIDTH, self.HEIGHT), Image.Resampling.BICUBIC)
			#Get size of image
			x, y = img.size
			#print('Debug New Image Size x : ',x,', y:',y) #Analyze the size of the out QSL  p.e x=843 , y= 537
		return img
	
	def run (self):
		""" Main function of the QSL class """
		
		#Load Text Font
		self.font=self.load_font()

		#Read photo image
		#self.img=self.read_image (self.source_image) 
		self.img=self.read_image (self.qsl_data['SOURCE_IMAGE']) 

		#Get size of image
		x, y = self.img.size

		#Resize image,  default QSL size x=843 , y= 537
		self.img=self.resize_image(x,y,self.img)

		# Creates objtect draw   
		self.draw = ImageDraw.Draw(self.img)

		#Create the bottom square containing contact data
		#self.creeCadre(self.WIDTH ,self.HEIGHT ,self.draw,self.color_frame,self.transparence)
		self.creeCadre(self.WIDTH ,self.HEIGHT ,self.draw,self.qsl_data['FRAME_COLOR'],self.qsl_data['TRANSPARENCE'])		


		#Write User , contact data QSL
		#self.write_user_data (self.draw,self.myXpos,self.myYpos,self.MySizeText,"black")
		#self.write_user_data (self.draw,self.myXpos,self.myYpos,self.MySizeText,self.color_text)
		self.write_user_data (self.draw,self.qsl_data['X_MY_CALL'],self.qsl_data['Y_MY_CALL'],self.qsl_data['SIZE_MY_CALL'],self.qsl_data['TEXT_COLOR'])		

		#Drawing in img
		draw = ImageDraw.Draw(self.img)

		#Show image
		self.img.show()

		# Save image with extension 
		ext= (self.qsl_data ['SOURCE_IMAGE']) .split(".")[-1]
		if (ext==""):
			ext="jpg"
		self.img.save( self.qsl_data ['CALL']+"."+ext)

				
if __name__ == "__main__":
	
	print ("soft version ", VERSION_SOFT) #Version logiciel
	app = InterfaceGraphique() #Instance InterfaceGraphique tkinter
	app.mainloop() #tkinter main loop			
