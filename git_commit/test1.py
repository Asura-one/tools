import curses
import os

ch = 0

while ch != ord("q"):
    screen = curses.initscr()
    screen.clear()
#    screen.border(0)

    for i in range(100):
        try:
            screen.addstr(i+1,0,os.popen("ps aux |awk 'NR==%s'" % i).read(),curses.A_NORMAL)
            screen.refresh()
        except:
            pass

    ch = screen.getch()

curses.endwin()
