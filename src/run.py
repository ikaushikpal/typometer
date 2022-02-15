import curses
from curses import wrapper
import time
import random
from text_gen import TextGenerator

TEXT_LENGTH = 25
global START_TIME
START_TIME = time.time()

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(2, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def load_text():
    txt = TextGenerator()
    generated_text = txt.generate(TEXT_LENGTH)
    return generated_text

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    
    wpm = 0

    stdscr.nodelay(False)

    while True:
        time_elapsed = max(time.time() - START_TIME, 1)
        
        wpm = round((TEXT_LENGTH*60)/time_elapsed)
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(True)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    game_start = False
    while True:
        wpm_test(stdscr)
        stdscr.addstr(3, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        if not game_start and ord(key) == 13:
            game_start = True
            
            START_TIME = time.time()
        if ord(key) == 27:
            break

wrapper(main)