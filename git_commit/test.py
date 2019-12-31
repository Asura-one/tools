#!/usr/bin/env python3
from os import system
import curses, subprocess

def get_param(prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(10, 10, 60)
    return input

def execute_cmd(cmd_string):
    system("clear")
    a = system(cmd_string)
    print("")
    if a == 0:
      print ("Command executed correctly")
    else:
      print ("Command terminated with error")
    raw_input("Press enter")
    print ("")

blacklist=['']

screen = curses.initscr()
curses.noecho();
curses.cbreak()
screen.keypad(1)
history = []
line = 0
column = 0
char = []
key = 0

screen.clear()
height,width = screen.getmaxyx()
#print (height,width)
subwin = screen.subwin(0, width, 0, 0)
subwin.box()
cliwin = screen.subwin(0, width, height-3, 0)
cliwin.box()

def menu(screen):
    height=0
    width = 30
    top=5
    left=3
    menuwin =screen.subwin(height , width,top ,left )
    menuwin.keypad(1)
    menuwin.border(0)
    menubar = ["1 - Add a user", "2 - Restart Apache", "3 - Show disk space", "Test", "Neo", "Netkiller""4 - Exit"]
    menuwin.addstr(1, 1, "Please enter a number...")

    current = 0
    while 1 :
        menuitem = 0
        #print (menuitem,current )
        menuwin.refresh()
        for m in menubar:
            if current == menuitem:
                menuwin.addstr(menuitem+2, 4,m , curses.A_REVERSE)
            else:
                menuwin.addstr(menuitem+2, 4, m)
            menuitem=menuitem+1

        key = menuwin.getch()
        if key == curses.KEY_UP:
            if current <= 0 :
                current = 0
            else:
                current = current-1
            #char = history[menuitem]
            #cliwin.clear()
            #cliwin.addstr(1,1,char)
            #print("up",line)
            #print(history[line])
        if key == curses.KEY_DOWN:
            if current >= len(menubar)-1 :
                current = len(menubar)-1
            else:
                current = current + 1
            #char = history[menuitem]
            #cliwin.clear()
            #cliwin.addstr(1,1,char)
            #print("down",line)
            #print(history[line])
        if key == 10:
            choice = current
            print(choice)
        #if key == 27:
        #   return

while key != ord('q'):

    screen.refresh()
    subwin = screen.subwin(0, width, 0, 0)
    subwin.box()
    cliwin = screen.subwin(0, width, height-3, 0)
    cliwin.box()


    key = screen.getch()

    #print(key)

    if 31<key<126:
        c=chr(key)
        char.append(c)
        #screen.addstr(2,2,c)
        cliwin.addstr(1,column+1,c)
        column = column+1
        #screen.refresh()
    else:
        pass                  # Ignore incorrect keys
    if key in (curses.KEY_ENTER,10):
        if len(char) > 1:
            cmd = ''.join(char)
            history.append(cmd)
            #system(cmd)
            subwin.clear()
            subwin.addstr(1,1,subprocess.getoutput(cmd))
            char = []
            line += 1
            column = 0
            cliwin.refresh()
            cliwin.clear()
            #print ("ENTER!!!")

    if key == curses.KEY_LEFT:
        curses.beep()
        print("left")
    if key == curses.KEY_RIGHT:
        curses.beep()
        print("right")
    if key == curses.KEY_UP:
        if line <= 0 :
            line = 0
        else:
            line = line-1
        char = history[line]
        cliwin.clear()
        cliwin.addstr(1,1,char)
        #print("up",line)
        #print(history[line])
    if key == curses.KEY_DOWN:
        if line !=0 or line > len(history)-1 :
            line = len(history)-1
        else:
            line = line+1
        char = history[line]
        cliwin.clear()
        cliwin.addstr(1,1,char)
        #print("down",line)
        #print(history[line])
    if key == curses.KEY_HOME:
        #subwin = screen.subwin(0, width, 0, 0)
        screen.addstr(1,1,'\n'.join(history))

    if key == curses.KEY_END:
        print(char)

    if key == 27:
        menu(screen)
    #KEY_BACKSPACE
    #KEY_NPAGE KEY_PPAGE
    # if x == ord('1'):
    #      username = get_param("Enter the username")
    #      homedir = get_param("Enter the home directory, eg /home/nate")
    #      groups = get_param("Enter comma-separated groups, eg adm,dialout,cdrom")
    #      shell = get_param("Enter the shell, eg /bin/bash:")
    #      curses.endwin()
    #      execute_cmd("useradd -d " + homedir + " -g 1000 -G " + groups + " -m -s " + shell + " " + username)
    # if x == ord('2'):
    #      curses.endwin()
    #      execute_cmd("apachectl restart")
    # if x == ord('3'):
    #      curses.endwin()
    #      execute_cmd("df -h")
    #
    #exit()
    #screen.refresh()
screen.keypad(0)
curses.echo() ; curses.nocbreak()
screen.clear()
curses.endwin()
