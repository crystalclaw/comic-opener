#!/usr/bin/env python3
import curses
import datetime
import webbrowser
import os
os.environ.setdefault('ESCDELAY', '25')

COMICCSV = os.path.dirname(os.path.realpath(__file__)) + '/comics.csv'
VERSION = '1.2.2'
LINE_LENGTH = 20


def mainMenu(datain):
    items = datain[0]
    options = ['Today    ', 'Monday   ', 'Tuesday  ', 'Wednesday', 'Thursday ',
               'Friday   ', 'Saturday ', 'Sunday   ', 'See all  ', 'Cancel   ']
    currentSelection = 0
    output = 0
    running = True
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(False)
    while running:
        stdscr.clear()
        stdscr.addstr('Comic opener ver. ' + VERSION + '\n\n')
        for i in range(len(options)):
            if i == currentSelection:
                stdscr.addstr(options[i] + '\n', curses.A_REVERSE)
            else:
                stdscr.addstr(options[i] + '\n')
        uinput = stdscr.getkey()
        if uinput == 'KEY_DOWN':
            if currentSelection >= (len(options) - 1):
                currentSelection = 0
            else:
                currentSelection += 1
        elif uinput == 'KEY_UP':
            if currentSelection <= 0:
                currentSelection = (len(options) - 1)
            else:
                currentSelection -= 1
        elif uinput == '\n':
            running = False
            if currentSelection == 0:
                output = getToday()
            if currentSelection == 1:
                output = 'M'
            if currentSelection == 2:
                output = 'T'
            if currentSelection == 3:
                output = 'W'
            if currentSelection == 4:
                output = 'Th'
            if currentSelection == 5:
                output = 'F'
            if currentSelection == 6:
                output = 'S'
            if currentSelection == 7:
                output = 'Su'
            if currentSelection == 8:
                    curses.nocbreak()
                    stdscr.keypad(False)
                    curses.echo()
                    curses.endwin()
                    if comicMenu(datain) == 'back':
                        mainMenu(datain)
                    else:
                        output = 'quit'
            if currentSelection == 9:
                output = 'quit'
            stdscr.clear()

    if currentSelection < 8:
        openDay(output, items)

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    return output


def comicMenu(comics):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(False)

    currentSelection = 0
    comicList = comics[1]
    selected = [' ']*len(comicList)
    running = True
    output = True
    while running:
        stdscr.clear()
        stdscr.addstr('Press O to open selected comics, A & C to (de)select all\
\n\n')
        stdscr.addstr('| |        Name        |M |T |W |Th|F |S |Su|\n')
        for i in range(len(comicList)):
            if i == currentSelection:
                stdscr.addstr('|' + selected[i] + formatForMenu(comicList[i])
                              + '\n', curses.A_REVERSE)
            else:
                stdscr.addstr('|' + selected[i] + formatForMenu(comicList[i])
                              + '\n')
        uinput = stdscr.getkey()
        if uinput == 'KEY_DOWN':
            if currentSelection >= (len(comicList) - 1):
                currentSelection = 0
            else:
                currentSelection += 1
        elif uinput == 'KEY_UP':
            if currentSelection <= 0:
                currentSelection = (len(comicList) - 1)
            else:
                currentSelection -= 1
        elif uinput == '\n':
            if selected[currentSelection] == 'X':
                selected[currentSelection] = ' '
            else:
                selected[currentSelection] = 'X'
        elif ord(uinput) == 27:
            # this^ is a bit of a hack to get the escape key; can't figure out
            # how to do it otherwise
            running = False
            output = 'back'
        elif uinput.lower() == 'o':
            running = False
            for i in range(len(selected)):
                if selected[i] == 'X':
                    webbrowser.open_new_tab(comicList[i][1])
        elif uinput.lower() == 'c':
            selected = [' ']*len(comicList)
        elif uinput.lower() == 'a':
            selected = ['X']*len(comicList)
        # else:
        #     stdscr.addstr('\n' + str(ord(uinput)))
        #     stdscr.getkey()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    return output


def formatForMenu(line):
    output = '|'
    spaces_to_add = LINE_LENGTH - len(line[0])
    # if spaces_to_add % 2 == 1:
    #     output = output + ' '
    # padding = (' ' * (spaces_to_add // 2))
    padding = (' ' * spaces_to_add)
    name = line[0].strip()
    if len(name) > LINE_LENGTH:
        name = name[0:17] + '...'
    output = output + name + padding + \
        '|' + line[2] + '|' + line[3] + '|' + line[4] + '|' + line[5] + '|' \
        + line[6] + '|' + line[7] + '|' + line[8] + '|'
    return output


def getToday():
    today = datetime.datetime.today().weekday()
    if today == 0:
        output = 'M'
    if today == 1:
        output = 'T'
    if today == 2:
        output = 'W'
    if today == 3:
        output = 'Th'
    if today == 4:
        output = 'F'
    if today == 5:
        output = 'S'
    if today == 6:
        output = 'Su'
    return output


def openDay(weekday, comicList):
    for i in comicList[weekday].values():
        webbrowser.open_new_tab(i)
        print(i)


def parseComics(comicFile):
    # comics = {weekday: {name: url}}
    comics = {'M': {}, 'T': {}, 'W': {}, 'Th': {}, 'F': {}, 'S': {}, 'Su': {}}
    comicsfile = open(comicFile, 'r')
    listofcomics = []
    for comic1 in comicsfile:
        comic = comic1.strip().split(',')
        current = [comic[0], comic[1]]
        if 'M' in comic[2:].upper():
            comics['M'][comic[0]] = comic[1]
            current.append('X ')
        else:
            current.append('  ')

        if 'T' in comic[2:].upper():
            comics['T'][comic[0]] = comic[1]
            current.append('X ')
        else:
            current.append('  ')

        if 'W' in comic[2:].upper():
            comics['W'][comic[0]] = comic[1]
            current.append('X ')
        else:
            current.append('  ')

        if 'TH' in comic[2:].upper():
            comics['Th'][comic[0]] = comic[1]
            current.append('X ')
        else:
            current.append('  ')

        if 'F' in comic[2:].upper():
            comics['F'][comic[0]] = comic[1]
            current.append('X ')
        else:
            current.append('  ')

        if 'S' in comic[2:]:
            comics['S'][comic[0]] = comic[1]
            current.append('X ')
        else:
            current.append('  ')

        if 'SU' in comic[2:].upper():
            comics['Su'][comic[0]] = comic[1]
            current.append('X ')
        else:
            current.append('  ')
        listofcomics.append(current)
    listofcomics = sorted(listofcomics)
    return [comics, listofcomics]

mainMenu(parseComics(COMICCSV))
