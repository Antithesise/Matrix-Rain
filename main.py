from matrix_rain import matrix_rain
from threading import Thread


with open("log.txt", "w") as f:
    f.truncate(0)


mr = matrix_rain() # create an instance of the class. This will automatically start the matrix_rain in a daemon thread.

input() # wait until user presses enter

exit() # matrix_rain is a daemon thread so it will exit when main thread does