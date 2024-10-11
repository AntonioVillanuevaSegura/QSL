"""
Antonio Villanueva Segura F4LEC
Program to edit a QSL the input arguments are as follows
STATION DATE UTC MHZ RST MOD
"""
import sys #Arguments
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#Default parameters
station ="EA3GRN"
date="26/07/68"
utc="12:00"
mhz="7.000"
rst ="59"
mode ="LSB"

print ("program use : python3 ", sys.argv[0], "STATION DATE UTC MHZ RST MODE ")

#Obtains arguments from the program execution

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
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", TEXT_SIZE, encoding="unic")

#Image Source
imageFile = "F4LEC.jpg"
img=Image.open(imageFile)


#Get size of image
x, y = img.size
print('Debug Image Size x : ',x,', y:',y) #Analyze the size of the incoming QSL

#Line Y of the text level
y_text=y-TEXT_SIZE-15

# Write text in image
draw = ImageDraw.Draw(img)

#Draw STATION 
draw.text((60, y_text), station ,BLACK,font=font)

#Draw DATE
draw.text((229, y_text), date ,BLACK,font=font)

#Draw HOUR
draw.text((380, y_text), utc ,BLACK,font=font)

#Draw Mhz
draw.text((500, y_text), mhz ,BLACK,font=font)

#Draw RST
draw.text((625, y_text), rst ,BLACK,font=font)

#Draw MODE
draw.text((690, y_text), mode ,BLACK,font=font)


draw = ImageDraw.Draw(img)
#img.show()
# Save image
img.save( "QSL_output.jpg")
