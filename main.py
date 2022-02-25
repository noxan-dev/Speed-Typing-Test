import random
import time
import threading
import PySimpleGUI as sg

speed = 0
EASY_WORD_COUNT = 10
EASY_TIMER = 60
words = []
sg.theme('DarkBlue2')
sg.set_options(font=("Courier New", 10))

with open('words') as f:
    for line in f.read().splitlines():
        words.append(line)

random_words = random.choices(words, k=EASY_WORD_COUNT)

layout = [[sg.Text("Start typing to track speed"), sg.Text(f"Speed: {speed}/WPM", auto_size_text=True, key="-SPEED-"),
           sg.Text(f"Time Left: {EASY_TIMER}", key="-TIMER-")],
          [sg.Text(random_words, auto_size_text=True, text_color='black', key="-WORDS-")],
          [sg.Multiline("", size=(30, 10), no_scrollbar=True, key='-TEXT-')],
          [sg.Button("Cancel", key='OK')]]


def countdown():
    timer = EASY_TIMER
    timer -= 1
    return timer

t = threading.Timer(1.0, countdown).start()

window = sg.Window("Speed Typing Test", layout, element_justification='center',
                   return_keyboard_events=True, use_default_focus=False)

dont_listen = ['BackSpace:8', 'Tab:9', 'Return:13', 'Shift:16', 'Control_L:17', 'Alt:18', 'PauseBreak:19',
               'Caps_Lock:20', 'Shift_L:16', 'Alt_L:18', 'Alt_R:18', 'Win_L:91', 'Down:40', 'Right:39', 'Left:37',
               'Up:38', 'MouseWheel:Up', 'MouseWheel:Down', 'Escape:27', '__TIMEOUT__']

completed_words = []
# ---===--- Loop taking in user input --- #
while True:

    event, values = window.read()
    window['-TIMER-'].update(f'Time Left: {t}')
    print(event, values)
    text_elem = window['-TEXT-']
    if event in ("OK", None) or EASY_TIMER == 0:
        completed_words.append(values['-TEXT-'].split(' '))
        print(event, "exiting")
        break
    if len(event) > 1:
        if event not in dont_listen:
            text_elem.update(value=text_elem.Get() + event)
    if event == ' ':
        if values['-TEXT-'] in words:
            window['-WORDS-'].update(text_color='green')
        else:
            window['-WORDS-'].update(text_color='red')

        # speed += 1
        # window['-SPEED-'].update(f"Speed: {speed}/WPM")


window.close()
