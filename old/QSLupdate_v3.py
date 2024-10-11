"""
Antonio Villanueva Segura F4LEC
Program to edit a QSL the input arguments are as follows
STATION DATE UTC MHZ RST MOD
"""
import sys #Arguments
import PIL
from PIL import ImageFont ,Image ,ImageDraw

#Default parameters
station ="EA3GRN"
date="26/07/68"
utc="12:00"
mhz="7.000"
rst ="59"
mode ="LSB"
transparence =False
source_image="F4LEC.jpg"

#default QSL size x=843 , y= 537
width=843
height=537
TEXT_SIZE=25

#Text Color 
BLACK = (0,0,0)
WHITE =(250,250,250)

def read_arguments () :
	"""Obtains arguments from the program execution"""
	global station,date,utc,mhz,rst,mode,transparence,source_image

	print ("Number args :" ,len(sys.argv))
	
	#print (sys.argv[0] ,sys.argv[5] )
	if (len(sys.argv) <5):
		print ("Error number of parameters , usage scheme")
		"""                      1      2    3   4   5   6  7 """
		print ( sys.argv[0], "STATION DATE UTC MHZ RST MODE Transparence {True or False} {Base image of the qsl} ")
		sys.exit()

	if len(sys.argv) >= 2:
		station=sys.argv[1]
	
	if len(sys.argv) >= 3:
		date=sys.argv[2]
		
	if len(sys.argv) >= 4:
		utc=sys.argv[3]
		
	if len(sys.argv) >= 5:
		mhz=sys.argv[4]
	
	""" RST 59"""
	if len(sys.argv) >= 6:
		rst=sys.argv[5]	
		
	""" mode usb lsb am fm """
	if len(sys.argv) >= 7:
		mode=sys.argv[6]
	
	""" Transparence True or False"""	
	if len(sys.argv) >= 8:
		tmp = (sys.argv[7]).lower()
		if "true" in tmp:
			print ("Transparence on")
			transparence =True 
		else:
			 print ("Transparence off")
	""" Name of the QSL base photo file """		 
	if len(sys.argv) >= 9:	
		source_image=sys.argv[8]	
		print ("Debug in read args ",source_image)	 
		
def read_image(fichier):
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
	
def load_font(taille=TEXT_SIZE):
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

def creeCadre(x, y, draw,color="black", transparent=False):
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

def write_user_data(draw,color=BLACK):
	#Line Y of the text level
	x=width #default
	y=height #default
	y_text=y-(y/8)+(TEXT_SIZE/2)-4
	
	#Draw STATION 
	draw.text((12, y_text), "STATION " ,color,font=font)

	#Draw DATE
	draw.text((122+30, y_text), "DATE" ,color,font=font)

	#Draw HOUR
	draw.text((260, y_text), "UTC" ,color,font=font)

	#Draw Mhz
	draw.text((380, y_text), "MHZ" ,color,font=font)

	#Draw RST
	draw.text((520, y_text), "RST" ,color,font=font)

	#Draw MODE
	draw.text((630, y_text), "MODE" ,color,font=font)

	#Draw QSL 
	draw.text((750, y_text), "QSL" ,color,font=font)


	y_text = y_text+TEXT_SIZE
	#Draw STATION 
	draw.text((12, y_text), station ,color,font=font)

	#Draw DATE
	draw.text((122, y_text), date ,color,font=font)

	#Draw HOUR
	draw.text((260, y_text), utc ,color,font=font)

	#Draw Mhz
	draw.text((380, y_text), mhz ,color,font=font)

	#Draw RST
	draw.text((520, y_text), rst ,color,font=font)

	#Draw MODE
	draw.text((630, y_text), mode ,color,font=font)

def resize_image(x,y,img):
	#Resize image
	print('Debug Org Image Size x : ',x,', y:',y) #Analyze the size of the out QSL  p.e x=843 , y= 537
	if (x!=width or y!=height) :	
		img = img.resize((width, height), Image.Resampling.BICUBIC)
		#Get size of image
		x, y = img.size
		print('Debug New Image Size x : ',x,', y:',y) #Analyze the size of the out QSL  p.e x=843 , y= 537
	return img

if __name__ == '__main__':				
	#Obtains arguments from the program execution
	read_arguments() 

	#Text Font
	font=load_font()

	img=read_image (source_image) #Read base image

	#Get size of image
	x, y = img.size

	img=resize_image(x,y,img)	#Resize image

	# Creates objtect draw   
	draw = ImageDraw.Draw(img)
	
	#Cadre
	creeCadre(width,height,draw,"black",transparence)
	
	#User data QSL
	write_user_data (draw)

	#Drawing in img
	draw = ImageDraw.Draw(img)
	
	#img = ImageDraw.Draw(img)
	
	#Show image
	img.show()

	# Save image
	img.save( "QSL_output.jpg")
