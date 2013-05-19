import curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.refresh()

key = ''
while key != ord('q'):
    key = stdscr.getch()
    stdscr.refresh()
    if key == curses.KEY_UP: 
        print "UP"
    elif key == curses.KEY_DOWN: 
        print "DOWN"
    print "Hi"
