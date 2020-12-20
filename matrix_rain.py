def matrix_rain(width="auto", height="auto", streams: (int) =60, minspeed: (int) =5, maxspeed: (int) =15, minlength: (int) =5, maxlength: (int) =20, randomness: (float) =10.00, characters: (str) ="\"*+-.012345789:<=>?Z¦╌コソヤ・二日｜ｰｱｳｴｵｶｷｸｹｻｼｽｾﾀﾂﾃﾅﾆﾇﾈﾊﾋﾍﾎﾏﾐﾑﾒﾓﾕﾗﾘﾜ") -> None :
	"""
	---
	Copyright @GoodCoderBadBoy 2020
	- width: an int of the width of the terminal in characters
	- height: an int of the height of the terminal in characters
	- streams: an int of the maximum number of streams that appear on screen at any time
	- minspeed: an int of the minimum # of characters that can travel down a row in a second
	- maxspeed: an int of the maximum # of characters that can travel down a row in a second
	- minlength: an int of the minimum stream length in characters
	- maxlength: an int of the maximum stream length in characters
	- randomness: a float of the maximum delay in seconds before a stream spawns at the start
	- characters: a string of the characters that will be displayed in the streams
	"""

	from os import system, get_terminal_size
	from threading import Thread
	from random import randrange
	from sys import platform
	from time import sleep

	occupied = {i:False for i in range(width if width != "auto" else get_terminal_size()[0])}

	def stream(occupied, width, height, minspeed, maxspeed, minlength, maxlength, randomness, characters):
		if randomness > 0:
			sleep(randrange(0, int(randomness * 100)) / 100)
		while True:
			column = randrange(0, width)
			while occupied[column] == True:
				column = randrange(0, width)
			occupied[column] = True
			length = randrange(minlength, maxlength + 1)
			rps = randrange(minspeed, maxspeed) + 1
			for y in range(-length, height):
				print(end="\u001b[H" + ("\u001b[" + str(y - 2) + "B" if y - 2 > 0 else "") + ("\u001b[" + str(column) + "C" if column else "") + "\u001b[48;2;0;10;0m  \u001b[0m", flush=True)
				for i in range(length):
					if y + i < height:
						print(end="\u001b[H" + ("\u001b[" + str(y + i) + "B" if y + i else "") + ("\u001b[" + str(column) + "C" if column else "") + "\u001b[48;2;0;10;0m  \u001b[0m\u001b[2D" + ("\u001b[38;2;155;255;155m\u001b[48;2;0;50;0m" if i == length - 1 else "\u001b[48;2;0;" + str(10 + (i * 2)) + ";0m\u001b[38;2;0;" + str(int(10 + ((254 / maxlength) * i))) + ";" + str(int((34 / maxlength) * i)) + "m") + characters[randrange(0, len(characters))] + "\u001b[0m")
				sleep(1/rps)
			print(end="\u001b[H\u001b[" + str(height - 1) + "B" + ("\u001b[" + str(column) + "C" if column else "") + "\u001b[48;2;0;10;0m  \u001b[0m", flush=True)
			occupied[column] = False

	system("cls" if platform == "win32" else "clear")
	print(end="\u001b[?25l\u001b[48;2;0;10;0m\u001b[H" + "\n".join([" " * ((width if width != "auto" else get_terminal_size()[0]) + 1) for i in range(height if height != "auto" else get_terminal_size()[1])]) + "\u001b[0m\u001b[H", flush=True)

	for thread in (threads := [Thread(target=stream, args=(occupied, (width if width != "auto" else get_terminal_size()[0]), (height if height != "auto" else get_terminal_size()[1]), minspeed, maxspeed, minlength, maxlength, randomness, characters, ), daemon=True) for i in range(streams)]):
		thread.start()
	for thread in threads:
		thread.join()
