import random
import time
import datetime
import threading
import PySimpleGUI as sg

speed = 0
EASY_WORD_COUNT = 1
EASY_TIMER = 60

minutes, seconds = (0, 20)
timer_format = datetime.timedelta(minutes=minutes, seconds=seconds)

words = []
sg.theme('DarkBlue2')
sg.set_options(font=("Courier New", 10))

layout = [[sg.Text("Start typing to track speed"), sg.Text(f"Speed: {speed}/WPM", auto_size_text=True, key="-SPEED-"),
           sg.Text(f"Time Left {timer_format}: ", key="-TIMER-")],
          [sg.Text('Start', auto_size_text=True, text_color='black', key="-WORDS-")],
          [sg.Multiline("", size=(30, 10), no_scrollbar=True, key='-TEXT-')],
          [sg.Button("Cancel", key='OK')]]


def countdown(minutes, seconds):
    timer = datetime.timedelta(seconds=seconds, minutes=minutes)
    while timer.seconds > 0:
        time.sleep(1)
        timer -= datetime.timedelta(seconds=1)
        window["-TIMER-"].Update(str(timer))
    window["-TIMER-"].Update("0:00:00")
    time.sleep(1)
    return 0


window = sg.Window("Speed Typing Test", layout, element_justification='center',
                   return_keyboard_events=True, use_default_focus=False)


def random_word_gen():
    with open('words') as f:
        data = f.readlines()
        random_words = random.choices(data, k=EASY_WORD_COUNT)
        random_words = [random_word.strip() for random_word in random_words]
        words.append(random_words)
    return random_words


dont_listen = ['BackSpace:8', 'Tab:9', 'Return:13', 'Shift:16', 'Control_L:17', 'Alt:18', 'PauseBreak:19',
               'Caps_Lock:20', 'Shift_L:16', 'Alt_L:18', 'Alt_R:18', 'Win_L:91', 'Down:40', 'Right:39', 'Left:37',
               'Up:38', 'MouseWheel:Up', 'MouseWheel:Down', 'Escape:27', '__TIMEOUT__']

completed_words = []
x = threading.Thread(target=countdown, args=(minutes, seconds), daemon=True).start()
# ---===--- Loop taking in user input --- #
while True:
    event, values = window.read()
    print(event, values)
    text_elem = window['-TEXT-']

    if event in ("OK", None):
        print(event, "exiting")
        print(completed_words)
        print(words)
        break
    if len(event) > 1:
        if event not in dont_listen:
            text_elem.update(value=str(event)[0])
    if ord(str(event)[0]) == 32:
        completed_words.append(values['-TEXT-'].split(' '))
        text_elem.update(value='')
        window['-WORDS-'].update(completed_words + random_word_gen())
        for word in completed_words:
            if word in words:
                window['-WORDS-'].update(text_color='green')
            else:
                window['-WORDS-'].update(text_color='red')
    # if x == "0:00:00":
    #     completed_words.append(values['-TEXT-'].split(' '))
    #     if completed_words == words:
    #         sg.popup("You completed all the words in the list")
    #     break
        # speed += 1
        # window['-SPEED-'].update(f"Speed: {speed}/WPM")


window.close()
