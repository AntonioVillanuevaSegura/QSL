# QSLupdate F4LEC  . Antonio Villanueva 

Simple program to create a QSL card from an image or photo.
The resulting qsl card has a size 843 x 537
Works with the following image formats 
*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp

[![QSLupdate](https://img.youtube.com/vi/Tt5WtEqMeTg/0.jpg)](https://www.youtube.com/watch?v=Tt5WtEqMeTg)

https://youtu.be/Tt5WtEqMeTg

In the graphic window at the top, we put our amateur radio callsign
The text appears on the left of the QSL with a default size of 80, 
but we can change the position and size.

In the middle window are the data of the callsign 
of the contacted radio amateur station, the date, time, frequency, RST

We just have to select our background image, which will resize to the appropriate size.
{Source Base Image}.

With dark background images it may be interesting to mark transparency

Notes: If you use the .bin executable file, 
the startup directory is located in tmp, so you will have to go to your /home 
or wherever the image is located. 
If instead you use the normal python execution python3 QSLupdate.py 
the search directory is where the executable is located.


The program  QSLupdate.py  is made in python 
Although I have generated an executable of this python code QSLupdate.bin

For execution in python3 you have to install some dependencies

	sudo apt-get install python3-pip
	sudo apt-get install python3-tk
	pip install tk
	pip install --upgrade Pillow



If you want to create an executable file from python, you can use Nuitka
First we need to install the different dependencies:

	sudo apt-get install patchelf
	python3 -m pip install -U nuitka

and then proceed to compilation

	python3 -m nuitka --standalone --onefile --enable-plugin=tk-inter QSLupdate.py


