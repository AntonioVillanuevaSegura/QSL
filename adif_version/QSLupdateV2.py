"""
Antonio Villanueva Segura F4LEC 
Program to edit & print a QSL the input arguments are as follows

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
VERSION_SOFT= "2.0 Adif"
MY_CALL ="F4LEC"
#DATE=datetime.datetime.today().strftime('%d/%m/%y')
DATE=datetime.datetime.today().strftime('%Y/%m/%d')

UTC=datetime.datetime.today().strftime('%H:%M')
BAND="40m"
MHZ="7.000"
RST ="59"
MODE ="SSB"
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
		self.qsl =QSL()
		
		#Adif class instance
		self.adif=Adif()
		
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
		self.iPosX=	tk.IntVar(self.FrameMyStation,value =1)	
		self.iPosY=	tk.IntVar(self.FrameMyStation,value =1)	
		self.iSizeText=	tk.IntVar(self.FrameMyStation,value =MY_TEXT_SIZE)	
				
		self.sCALL=tk.StringVar(self.FrameSup,value =MY_CALL)	
		self.sDate=tk.StringVar(self.FrameSup,value =DATE)	
		self.sUtc=tk.StringVar(self.FrameSup,value =UTC)
		self.sBAND=tk.StringVar(self.FrameSup,value =BAND)
		self.sMhz=tk.StringVar(self.FrameSup,value =MHZ)
		self.sRST_SEND=tk.StringVar(self.FrameSup,value =RST)
		self.sRST_RCVD=tk.StringVar(self.FrameSup,value =RST)		
		self.sMode=tk.StringVar(self.FrameSup,value =MODE)	
		self.sGRIDSQUARE=tk.StringVar(self.FrameSup,value =GRIDSQUARE)
		self.sQSLMSG=tk.StringVar(self.FrameSup,value =QSLMSG)
		#self.sQSL_SENT=tk.StringVar(self.FrameSup,value ='Y')			
		
		self.bTransparence=tk.BooleanVar(self.FrameSup,value =TRANSPARENCE)
		self.sSource_image=tk.StringVar(self.FrameSup,value =SOURCE_IMAGE)
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
			
		

		#Frame Sup Labels QSO CONTACT 
		"""CALL BAND MODE RST_SENT RST_RCVD QSL_SENT QSL_SENT_VIA QSLMSG APP_EQSL_AG
		   GRIDSQUARE EQSL_QSL_RCVD EQSL_QSLRDATE """
		   
		labelCALL = tk.Label(self.FrameSup, text="CALL", anchor="center")
		labelCALL.grid(row=0, column=0, padx=4, pady=4)

		
		labelGRIDSQUARE = tk.Label(self.FrameSup, text="GRIDSQUARE", anchor="center")
		labelGRIDSQUARE.grid(row=0, column=1, padx=4, pady=4)		
		
		labelDate = tk.Label(self.FrameSup, text="YYYYMMDD", anchor="center")
		labelDate.grid(row=0, column=2, padx=4, pady=4)
		
		labelUtc = tk.Label(self.FrameSup, text="UTC", anchor="center")
		labelUtc.grid(row=0, column=3, padx=4, pady=4)
		
		labeBAND = tk.Label(self.FrameSup, text="BAND", anchor="center")
		labeBAND.grid(row=0, column=4, padx=4, pady=4)
		
		labelMhz = tk.Label(self.FrameSup, text="Mhz", anchor="center")
		labelMhz.grid(row=0, column=5, padx=4, pady=4)
		
		labelRST_SENT = tk.Label(self.FrameSup, text="RST RX", anchor="center")
		labelRST_SENT.grid(row=0, column=6, padx=4, pady=4)
		
		labelRST_RCVD = tk.Label(self.FrameSup, text="RST TX" ,anchor="center")
		labelRST_RCVD.grid(row=0, column=7, padx=4, pady=4)		
		
		
		labelMODE = tk.Label(self.FrameSup, text="MODE", anchor="center")
		labelMODE.grid(row=0, column=8, padx=4, pady=4)	
		
		labelQSL_SENT = tk.Label(self.FrameSup, text="QSL_SENT", anchor="center")
		labelQSL_SENT.grid(row=0, column=9, padx=4, pady=4)			
				
		#FrameSup Entries  QSO CONTACT 	
		self.CALL=tk.Entry(self.FrameSup,textvariable=self.sCALL,justify='center',bg="white",width=15)
		self.CALL.grid(row=1,column=0)		
		
		self.GRIDSQUARE=tk.Entry(self.FrameSup,textvariable=self.sGRIDSQUARE,justify='center',bg="white",width=10)
		self.GRIDSQUARE.grid(row=1,column=1)			
		
		self.Date=tk.Entry(self.FrameSup,textvariable=self.sDate,justify='center',bg="white",width=10)
		self.Date.grid(row=1,column=2)	
		
		self.Utc=tk.Entry(self.FrameSup,textvariable=self.sUtc,justify='center',bg="white",width=7)
		self.Utc.grid(row=1,column=3)	
		
		"""
		self.BAND=tk.Entry(self.FrameSup,textvariable=self.sBAND,justify='center',bg="white",width=10)
		self.BAND.grid(row=1,column=3)
		"""
	
		
		vBAND = ('2222m 0,1357-0,1378','630m 0,472-0,479','160m 1,810-1,850',
		'80m 3,500-3,800','60m 5,3515-5,3665','40m 7,000-7,200',
		'30m 10,100-10,150','20m 14,000-14,350','17m 18,068-18,168',
		'15m 21,000-21,450','12m 24,890-24,990','11m CB','10m 28,000-29,700',
		'6m 50,000-52,000','4m 70-70,500 MHz','2m 144-146','1,35m',
		'70cm 430-440','23cm 1240-1300','13cm 2300-2450','9cm','6cm 5650-5850',
		'5cm','3cm 10000-10500','1,2cm 24000-24250','6mm 47000-4720',
		'4mm 76000-81500','2,4mm 122250-123000','2mm 134000-141000','1,2mm 241000-250000')
		self.BAND = ttk.Combobox(self.FrameSup, values=vBAND, width=19, justify='center')
		self.BAND.grid(row=1, column=4)
		
		self.BAND.set(vBAND[5])
		
		self.BAND['state'] = 'readonly'		
		
		#Bind combo - event changer tk.Entry self.Mhz
		self.BAND.bind("<<ComboboxSelected>>", self.update_MhzEntry)
		
		
		self.Mhz=tk.Entry(self.FrameSup,textvariable=self.sMhz,justify='center',bg="white",width=10)
		self.Mhz.grid(row=1,column=5)
		
		self.RST_RCVD=tk.Entry(self.FrameSup,textvariable=self.sRST_RCVD,justify='center',bg="white",width=5)
		self.RST_RCVD.grid(row=1,column=6)	

		self.RST_SEND=tk.Entry(self.FrameSup,textvariable=self.sRST_SEND,justify='center',bg="white",width=5)
		self.RST_SEND.grid(row=1,column=7)		
		
		#self.MODE=tk.Entry(self.FrameSup,textvariable=self.sMode,justify='center',bg="white",width=5)
		#self.MODE.grid(row=1,column=8)	
		
		vMODE = ("CW","AM","FM","SSB", "RTTY", "RTTYM","SSTV","FT8","PSK", 
		"PSK2K", "ARDOP", "ATV", "C4FM", "CHIP", "CLO", "CONTESTI",
		 "DIGITALVOICE", "DOMINO", "DSTAR", "FAX", "FSK441", "HELL",
		 "ISCAT", "JT4", "JT6M", "JT9", "JT44", "JT65", "MFSK", "MSK144", "MT63",
		 "OLIVIA", "OPERA", "PAC", "PAX", "PKT",  "Q15", "QRA64",
		 "ROS",  "T10", "THOR", "THRB", "TOR",
		  "V4", "VOI", "WINMOR", "WSPR")
		
		self.MODE = ttk.Combobox(self.FrameSup, values=vMODE, width=12, justify='center')
		self.MODE.grid(row=1, column=8)
		
		self.MODE.set(vMODE[3])
		
		self.MODE['state'] = 'readonly'	
		
		self.MODE.bind("<<ComboboxSelected>>", self.update_Mode)
		
		
		self.FrameSup.grid_columnconfigure(0, weight=0)
		"""
		self.QSL_SENT=tk.Entry(self.FrameSup,textvariable=self.sQSL_SENT,justify='center',bg="white",width=5)
		self.QSL_SENT.grid(row=1,column=8)		
		"""
		
		vQSL_SENT = ('Y','N')
		self.QSL_SENT = ttk.Combobox(self.FrameSup, values=vQSL_SENT, width=5, justify='center')
		self.QSL_SENT.grid(row=1, column=9)
		
		self.QSL_SENT.set(vQSL_SENT[1])
		
		self.QSL_SENT['state'] = 'readonly'
		
		#Frame Med Source Image Colors  ...
		
		labelSourceImage = tk.Label(self.FrameMed, text="Source Base Image", anchor="center")
		labelSourceImage.grid(row=0, column=1, sticky="e", padx=4, pady=4)	
		
		self.SourceImage=tk.Entry(self.FrameMed,textvariable=self.sSource_image,justify='center',bg="white")
		self.SourceImage.grid(row=1,column=1)	
		
		# Vinculo  -> método browse_folder
		#self.SourceImage.bind("<FocusIn>", self.browser_folder)		
		self.SourceImage.bind("<Button-1>", self.browser_folder)	
		
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
		self.qsl.set_mystation (self.sMY_CALL.get())
		self.qsl.set_Xpos (self.iPosX.get())
		self.qsl.set_Ypos (self.iPosY.get())	
		self.qsl.set_SizeText (self.iSizeText.get())			
		
		#QSL contact
		self.qsl.set_station (self.sCALL.get())
		self.qsl.set_date (self.sDate.get())
		self.qsl.set_utc (self.sUtc.get())
		self.qsl.set_mhz (self.sMhz.get())
		self.qsl.set_rst (self.sRST_SEND.get())
		self.qsl.set_mode (self.sMode.get())
		
		self.qsl.set_transparence(self.bTransparence.get())
		self.qsl.set_source_image (self.sSource_image.get() )
		self.qsl.set_text_color(self.sTextColor.get())
		self.qsl.set_frame_color(self.sFrameColor.get())
		
		#Adif
		#Create QSL contact				
		contact = {#Contact model QSO adif version eqsl
			'CALL': self.sCALL.get(),
			'QSO_DATE':self.sDate.get(),
			'TIME_ON':self.sUtc.get(),			
			'BAND': self.sBAND.get(),
			'MODE': self.sMode.get(),
			'RST_SENT': self.sRST_SEND.get(),
			'RST_RCVD': self.sRST_RCVD.get(),
			'QSL_SENT': self.QSL_SENT.get(),
			'QSL_SENT_VIA':'e',
			'QSLMSG':self.sQSLMSG.get(),
			'APP_EQSL_AG':'',
			'GRIDSQUARE':self.sGRIDSQUARE.get(),
			'EQSL_QSL_RCVD':'',
			'EQSL_QSLRDATE':''
		}
		
		#Adif Set data QSO contact
		(self.adif).set_contact(contact)
		
		#Adif Cree  le string Adif et ecrire adif
		(self.adif).creer_adif()

		#Make the graphic QSL													
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
	
	def update_MhzEntry(self, event):
		"""Updates the Mhz input based on the selected band """

		value = self.BAND.get()
		
		array_value = re.split(r'[\s-]+', value)
		#self.sBAND=array_value[0] # update variable sBAND adif
		self.sBAND.set (array_value[0]) # update variable sBAND adif
		self.Mhz.delete(0, tk.END)
		if len(array_value) >=2:
			self.Mhz.insert(0, array_value[1])				
		else:
			self.Mhz.insert(0,"")
	
	def update_Mode (self,event):
		self.sMode.set (self.MODE.get()	)
					
class QSL():
	""" This class is the heart of the creation of the QSL card """
	def __init__(self):		
		self.MY_CALL=None
		self.myXpos=None
		self.myYpos=None
		self.MySizeText=None
		
		self.CALL =None
		self.date=None
		self.utc=None
		self.mhz=None
		self.RST_SEND=None
		self.MODE=None
		self.transparence=False
		self.source_image=SOURCE_IMAGE
		self.image=None
		self.draw=None
		self.font=None
		
		self.color_frame=None
		self.color_text=None
		
		#default QSL size x=843 , y= 537
		self.WIDTH=843
		self.HEIGHT=537
		self.TEXT_SIZE=25

	#setters  To configure the different variables
	def set_mystation(self,data):
		self.MY_CALL=data
		
	def set_Xpos(self,data):
		self.myXpos=data	
		
	def set_Ypos(self,data):
		self.myYpos=data	
		
	def set_SizeText(self,data):
		self.MySizeText=data					
		
	def set_station(self,data):
		self.CALL=data
		
	def set_date (self,data):
		#YYMMDD
		self.date=data[2:]
		
	def set_utc (self,data):
		self.utc=data
		
	def set_mhz (self,data):
		self.mhz=data	
		
	def set_rst (self,data):
		self.RST_SEND=data	
		
	def set_mode (self,data):
		self.MODE=data											
	 
	def set_source_image (self,data):
		self.source_image =data
		
	def set_transparence (self,data):
		self.transparence =data	
	
	def set_frame_color	(self,data):
		self.color_frame=data
		
	def set_text_color	(self,data):
		self.color_text=data		
		
	def read_image(self,fichier):
		"""Read base image  """
		print ("DEBUG base file image :" ,fichier)
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

		#Draw QSL 
		draw.text((750, y_text), "QSL" ,color,font=self.font)


		y_text = y_text+TEXT_SIZE+6
		#Draw STATION 
		draw.text((12, y_text), self.CALL ,color,font=self.font)

		#Draw DATE
		draw.text((122, y_text), self.date ,color,font=self.font)

		#Draw HOUR
		draw.text((260, y_text), self.utc ,color,font=self.font)

		#Draw Mhz
		draw.text((380, y_text), self.mhz ,color,font=self.font)

		#Draw RST
		draw.text((520, y_text), self.RST_SEND ,color,font=self.font)

		#Draw MODE
		draw.text((630, y_text), self.MODE ,color,font=self.font)
		

		#Maximum size control for the position and size of my text 
		if myX>self.WIDTH:
			myX=( self.WIDTH - mySizeText*3 )
		
		if myY >self.HEIGHT:
			myY= ( self.HEIGHT -mySizeText  -10 )
		
		#Write my station's data in the QSL
		self.font=self.load_font(mySizeText)
		draw.text((myX, myY), self.MY_CALL ,color,font=self.font)		
		
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
		self.creeCadre(self.WIDTH ,self.HEIGHT ,self.draw,self.color_frame,self.transparence)


		#Write User , contact data QSL
		#self.write_user_data (self.draw,self.myXpos,self.myYpos,self.MySizeText,"black")
		self.write_user_data (self.draw,self.myXpos,self.myYpos,self.MySizeText,self.color_text)

		#Drawing in img
		draw = ImageDraw.Draw(self.img)

		#Show image
		self.img.show()

		# Save image with extension 
		ext= (self.source_image) .split(".")[-1]
		if (ext==""):
			ext="jpg"
		self.img.save( self.CALL+"."+ext)

class Adif():
	""" Classe pour ecrire l'Adif dans un fichier externe  vous devez saisir les données du qso"""
	def __init__(self):	
		self.contact = {
			'CALL': None,
			'QSO_DATE':None,
			'TIME_ON':None,
			'BAND': None,
			'MODE': None,
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
		self.programid="F4LEC_soft"
		self.adif_version="3.1.0"
		self.adif=None #Text adif
		self.fichier='mi_log.adi' #Nom fichier externe
		self.data=None
		self.heure=None
	
	def valeur_vide(self,valeur):
		""" valeur null"""
		return valeur is None	
	
	def set_contact (self,contact):
		""" Set self.contact local avec dict. contact externe dict."""
		for key,value in contact.items():
			self.contact[key]=value
			
	def creer_adif(self):
		"""Créer une chaîne adif  """
		# check l'existence du fichier adif 
		check = self.check()
		
		maintenant = datetime.datetime.now()

		#date =  maintenant.strftime("%Y%m%d")
		#heure =  maintenant.strftime("%H%M%S")
		#heure =  maintenant.strftime("%H%M")
		
		self.adif=""
		if (not self.valeur_vide(self.programid) and not (check)):
			self.adif =f"<PROGRAMID:{len(self.programid)}>{self.programid}\n"
			
		if (not self.valeur_vide(self.adif_version)  and not (check)):						
			self.adif +=f"<ADIF_Ver:{len(self.adif_version)}>{self.adif_version}\n"
		
		if ( not (check)):	
			self.adif += "<EOH>\n"
			
		if not(self.valeur_vide(self.contact['CALL'])):
			self.adif += f"<CALL:{len(self.contact['CALL'])}>{self.contact['CALL']}"
			
		if not(self.valeur_vide(self.contact["QSO_DATE"])):
			self.contact["QSO_DATE"] = ''.join(filter(str.isdigit, self.contact["QSO_DATE"]))
			self.adif += f"<QSO_DATE:{ len( str (self.contact['QSO_DATE']))}>{self.contact['QSO_DATE']}"
			
		if not(self.valeur_vide(str (self.contact['TIME_ON']))):	
			#self.contact["TIME_ON"] =self.contact["TIME_ON"] .replace(':', '')	
			self.contact["TIME_ON"] = ''.join(filter(str.isdigit, self.contact["TIME_ON"]))
			self.adif += f"<TIME_ON:{ len( str (self.contact['TIME_ON']))}>{self.contact['TIME_ON']}"
			
		if not(self.valeur_vide(self.contact['BAND'])):		
			self.adif += f"<BAND:{len(self.contact['BAND'])}>{self.contact['BAND']}"
			
		if not(self.valeur_vide(self.contact['MODE'])):		
			self.adif += f"<MODE:{len(self.contact['MODE'])}>{self.contact['MODE']}"
			
		if not(self.valeur_vide(self.contact['RST_SENT'])):		
			self.adif += f"<RST_SENT:{len(self.contact['RST_SENT'])}>{self.contact['RST_SENT']}"
			
		if not(self.valeur_vide(self.contact['RST_RCVD'])):		
			self.adif += f"<RST_RCVD:{len(self.contact['RST_RCVD'])}>{self.contact['RST_RCVD']}"
			
		if not(self.valeur_vide(self.contact['QSL_SENT'])):		
			self.adif += f"<QSL_SENT:{len(self.contact['QSL_SENT'])}>{self.contact['QSL_SENT']}"	
			
		if not(self.valeur_vide(self.contact['QSL_SENT_VIA'])):		
			self.adif += f"<QSL_SENT_VIA:{len(self.contact['QSL_SENT_VIA'])}>{self.contact['QSL_SENT_VIA']}"
			
		if not(self.valeur_vide(self.contact['QSLMSG'])):		
			self.adif += f"<QSLMSG:{len(self.contact['QSLMSG'])}>{self.contact['QSLMSG']}"
				
		if not(self.valeur_vide(self.contact['APP_EQSL_AG'])):		
			self.adif += f"<APP_EQSL_AG:{len(self.contact['APP_EQSL_AG'])}>{self.contact['APP_EQSL_AG']}"
				
		if not(self.valeur_vide(self.contact['GRIDSQUARE'])):		
			self.adif += f"<GRIDSQUARE:{len(self.contact['GRIDSQUARE'])}>{self.contact['GRIDSQUARE']}"
				
		if not(self.valeur_vide(self.contact['EQSL_QSL_RCVD'])):		
			self.adif += f"<EQSL_QSL_RCVD:{len(self.contact['EQSL_QSL_RCVD'])}>{self.contact['EQSL_QSL_RCVD']}"
			
		if not(self.valeur_vide(self.contact['EQSL_QSLRDATE'])):		
			self.adif += f"<EQSL_QSLRDATE:{len(self.contact['EQSL_QSLRDATE'])}>{self.contact['EQSL_QSLRDATE']}"					
		self.adif += "<EOR>\n"
		
		self.write () #Ecrire Adif dans un fichier externe
		
		return self.adif

	def write(self):
		""" write adif file with adif data """
		with open(self.fichier, 'a') as fichier:
			fichier.write(self.adif)
			
	def exist_file(self):
		""" Check for the existence of a file use in check  """
		if os.path.exists(self.fichier):
			return True
		else:
			return False
								
	def check(self):	
		""" analyse l'existence du fichier et son contenu"""
		if not (self.exist_file ()):
			return False	
		
		# open fichier
		try:
			with open(self.fichier, 'r') as text:
				contenu = text.read()
		except IOError as e:
			return False
				
		# test words in fichier 
		# Check PROGRAMID ADIF_Ver EOH 
		tests=("PROGRAMID","ADIF_Ver","EOH")
		
		for test in tests:
			if test in contenu :
				return True
		
		return False		
				
if __name__ == "__main__":
	
	print ("soft version ", VERSION_SOFT) #Version logiciel
	app = InterfaceGraphique() #Instance InterfaceGraphique tkinter
	app.mainloop() #tkinter main loop			
