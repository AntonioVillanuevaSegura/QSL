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

#default QSL size x=843 , y= 537
width=843
height=537
TEXT_SIZE=25



def load_font(taille=TEXT_SIZE):
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

"""
def creeCadre(x,y,draw):
	x0=0
	x1=x
	
	y0=y-(y/8)
	y1=y
	# Dibuja el cuadrado blanco
	#draw.rectangle([x0, y0, x1, y1], outline="black", width=2)
	draw.rectangle([x0, y0, x1, y1], fill="white", outline="black", width=2)

	# Dibuja seis líneas verticales dentro del cuadrado
	num_vertical_lines = 6
	line_spacing = (x1 - x0) / (num_vertical_lines + 1)

	for i in range(1, num_vertical_lines + 1):
		x = x0 + i * line_spacing
		draw.line([(x, y0), (x, y1)], fill="black", width=1)

	# Dibuja una línea horizontal dentro del cuadrado
	horizontal_y = (y0 + y1) / 2
	draw.line([(x0, horizontal_y), (x1, horizontal_y)], fill="black", width=1)
"""
def creeCadre(x, y, draw, transparent=False):
    x0 = 0
    x1 = x
    y0 = y - (y / 8)
    y1 = y

    # Definir el color de relleno
    if transparent:
        fill_color = (255, 255, 255, 0)  # Completamente transparente
    else:
        fill_color = (255, 255, 255, 255)  # Blanco opaco

    # Dibuja el rectángulo
    draw.rectangle([x0, y0, x1, y1], fill=fill_color, outline="black", width=2)

    # Dibuja seis líneas verticales dentro del rectángulo
    num_vertical_lines = 6
    line_spacing = (x1 - x0) / (num_vertical_lines + 1)

    for i in range(1, num_vertical_lines + 1):
        x_line = x0 + i * line_spacing
        draw.line([(x_line, y0), (x_line, y1)], fill="black", width=1)

    # Dibuja una línea horizontal dentro del rectángulo
    horizontal_y = (y0 + y1) / 2
    draw.line([(x0, horizontal_y), (x1, horizontal_y)], fill="black", width=1)

#Obtains arguments from the program execution

if (len(sys.argv) <7):
	print ("Error number of arguments !")
	print ("program use :", sys.argv[0], "STATION DATE UTC MHZ RST MODE ")
	sys.exit()

if len(sys.argv) >=2:
	station=sys.argv[1]
	
if len(sys.argv) >=3:
	date=sys.argv[2]
	
if len(sys.argv) >=4:
	utc=sys.argv[3]
	
if len(sys.argv) >=5:
	mhz=sys.argv[4]
	
if len(sys.argv) >=6:
	rst=sys.argv[5]	
	
if len(sys.argv) >=7:
	mode=sys.argv[6]				


#Text Color 
BLACK = (0,0,0)
WHITE =(250,250,250)
TEXT_SIZE=25

"""
/usr/share/fonts/truetype/freefont/
FreeMonoBoldOblique.ttf  FreeSansBoldOblique.ttf  FreeSerifBoldItalic.ttf
FreeMonoBold.ttf         FreeSansBold.ttf         FreeSerifBold.ttf
FreeMonoOblique.ttf      FreeSansOblique.ttf      FreeSerifItalic.ttf
FreeMono.ttf             FreeSans.ttf             FreeSerif.ttf

"""
#Text Font

#font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", TEXT_SIZE, encoding="unic")
font=load_font()

#Image default Source
imageFile = "F4LEC.jpg"

#Try open image
try:
	img=Image.open(imageFile)
except IOError:
    print("Impossible d'ouvrir l'image .arrière-plan blanc par défaut")
    img = Image.new("RGB", (width, height), "white")


#Get size of image
x, y = img.size
print('Debug Image Size x : ',x,', y:',y) #Analyze the size of the incoming QSL  p.e x=843 , y= 537

#Resize image
if (x!=width or y!=height) :	
	img = img.resize((width, height), Image.Resampling.BICUBIC)
	#Get size of image
	x, y = img.size
	print('Debug New Image Size x : ',x,', y:',y) #Analyze the size of the incoming QSL  p.e x=843 , y= 537
	
#Line Y of the text level
y_text=y-(y/8)+(TEXT_SIZE/2)-4

# Write text in image
draw = ImageDraw.Draw(img)

creeCadre(x,y,draw,True)

#Draw STATION 
draw.text((12, y_text), "STATION " ,BLACK,font=font)

#Draw DATE
draw.text((122+30, y_text), "DATE" ,BLACK,font=font)

#Draw HOUR
draw.text((260, y_text), "UTC" ,BLACK,font=font)

#Draw Mhz
draw.text((380, y_text), "MHZ" ,BLACK,font=font)

#Draw RST
draw.text((520, y_text), "RST" ,BLACK,font=font)

#Draw MODE
draw.text((630, y_text), "MODE" ,BLACK,font=font)

#Draw QSL 
draw.text((750, y_text), "QSL" ,BLACK,font=font)


y_text = y_text+TEXT_SIZE
#Draw STATION 
draw.text((12, y_text), station ,BLACK,font=font)

#Draw DATE
draw.text((122, y_text), date ,BLACK,font=font)

#Draw HOUR
draw.text((260, y_text), utc ,BLACK,font=font)

#Draw Mhz
draw.text((380, y_text), mhz ,BLACK,font=font)

#Draw RST
draw.text((520, y_text), rst ,BLACK,font=font)

#Draw MODE
draw.text((630, y_text), mode ,BLACK,font=font)

#Drawing in img
draw = ImageDraw.Draw(img)

img.show()
# Save image
img.save( "QSL_output.jpg")
