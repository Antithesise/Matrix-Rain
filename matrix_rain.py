class matrix_rain:
    def __init__(self, width: int | None=None, height: int | None=None, streams: int=60, minspeed: int=5, maxspeed: int=15, minlength: int=5, maxlength: int=20, randomness: float=10.00, characters: str="\"*+-.012345789:<=>?Z¦╌コソヤ・二日｜ｰｱｳｴｵｶｷｸｹｻｼｽｾﾀﾂﾃﾅﾆﾇﾈﾊﾋﾍﾎﾏﾐﾑﾒﾓﾕﾗﾘﾜ") -> None:
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
        - randomness: a float of the maximum delay in seconds before a stream spawns at the start aswell as how often a character in a stream may change
        - characters: a string of the characters that will be displayed in the streams
        """
        
        from os import get_terminal_size
        from threading import Thread
        from atexit import register
        

        width = width or get_terminal_size()[0]
        height = height or get_terminal_size()[1]

        register(print, end=f"\x1b[1000A\r\x1b[{height+1}B")

        Thread(
            target=self.matrix_rain,
            args=(
                width, height, streams, minspeed, maxspeed, minlength, maxlength, randomness, characters,
            ),
            daemon=True
        ).start()

    def matrix_rain(self, width: int, height: int, streams: int, minspeed: int, maxspeed: int, minlength: int, maxlength: int, randomness: float, characters: str) -> None :
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
        - randomness: a float of the maximum delay in seconds before a stream spawns at the start aswell as how often a character in a stream may change
        - characters: a string of the characters that will be displayed in the streams
        """

        from random import randrange, choice
        from threading import Thread
        from sys import platform
        from time import sleep
        from os import system

            
        occupied = {i:False for i in range(width)}

        def stream(occupied, width, height, minspeed, maxspeed, minlength, maxlength, randomness, characters, thread_id=0):
            if randomness > 0:
                sleep(
                    randrange(
                        0,
                        round(
                            randomness * 100
                        )
                    ) / 100
                )

            while True:
                column = randrange(0, width)

                while occupied[column] == True:
                    column = randrange(0, width)

                occupied[column] = True
                length = randrange(minlength, maxlength + 1)
                rps = randrange(minspeed, maxspeed) + 1

                chrlist: list[str] = [choice(characters) for i in range(height)]

                for y in range(-length, height): # -length is used so that the stream starts above the top border.
                    print(
                        end="\x1b[H" + (
                            "\x1b[" + str(y - 2) + "B" if y - 2 > 0 else ""
                        ) + (
                            "\x1b[" + str(column) + "C" if column else ""
                        ) + "\x1b[48;2;0;10;0m  \x1b[0m",
                        flush=True
                    )
                    
                    for i in range(length):
                        if y + i < height:
                            print(
                                end="\x1b[H" + (
                                    f"\x1b[{y + i}B" if y + i else ""
                                ) + (
                                    f"\x1b[{column}C" if column else ""
                                ) + "\x1b[48;2;0;10;0m  \x1b[0m\x1b[2D" + (
                                    "\x1b[38;2;155;255;155m\x1b[48;2;0;50;0m" if i == length - 1 else f"\x1b[48;2;0;{min(10 + (i * 2), 255)};0m\x1b[38;2;0;{min(round(10 + ((254 / maxlength) * i)), 255)};{min(round((34 / maxlength) * i), 255)}m"
                                ) + chrlist[y + i] + "\x1b[0m"
                            )
                    
                    if randrange(0, 15 - randomness) == 0: # 1 /5 chance (default)
                        n = randrange(y, min(y + length, len(chrlist)))
                        chrlist[n] = choice(characters) # replace a random chr in the string with another

                    sleep(1/rps)

        system("cls" if platform == "win32" else "clear") # clear terminal
        print(
            end=f"\x1b[48;2;0;10;0m\x1b[H{chr(10).join([' ' * (width + 1) for i in range(height)])}\x1b[0m\x1b[H",
            flush=True
        ) # fill output area (specified by width and height args) with colour #000A00 and move cursor to top left hand corner

        threads: list[Thread] = []

        for i in range(streams):
            Thread(
                target=stream,
                args=(
                    occupied, width, height, minspeed, maxspeed, minlength, maxlength, randomness, characters, i
                ),
                daemon=True
            ).start()
