from sys import stdout, exit, argv
from getopt import getopt, GetoptError
from attendance.attendance import Attendance

def main(argv):
    """Arguments: width height posX posY"""
    width = 400
    height = 400
    x = 0
    y = 0
    usage = 'Usage: main.py [-w <width>] [-h <height>] [-x <posX>] [-y <posY>]'

    try:
        opts, _ = getopt(argv, "w:h:x:y:", ["help", "width=", "height=", "posx=", "posy="])
    except GetoptError:
        print(usage)
        exit(2)

    for opt, arg in opts:
        if opt == '--help':
            print(usage)
            exit()
        elif opt in ("-w", "--width"):
            width = arg
        elif opt in ("-h", "--height"):
            height = arg
        elif opt in ("-x", "--posx"):
            x = arg
        elif opt in ("-y", "--posy"):
            y = arg

    at = Attendance("TOMi", int(width), height, x, y)

    at.startLoop()

    stdout.write("exit\n")
    stdout.flush()

if __name__ == "__main__":
    main(argv[1:])
