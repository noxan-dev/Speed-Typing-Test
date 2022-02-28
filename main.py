import datetime
import random
import threading
import time
import PySimpleGUI as sg

wpm = 0
EASY_WORD_COUNT = 1
EASY_TIMER = 60

minutes, seconds = (0, EASY_TIMER)
timer_format = datetime.timedelta(minutes=minutes, seconds=seconds)

sg.theme('DarkBlue2')
sg.set_options(font=("Courier New", 10))

layout = [[sg.Text("Start typing to track speed"), sg.Text(f"Speed: {wpm}/WPM", auto_size_text=True, key="-SPEED-"),
           sg.Text(f"Time Left {timer_format}: ", key="-TIMER-")],
          [sg.Text('Start', auto_size_text=True, text_color='black', key="-WORDS-")],
          [sg.Multiline("", size=(30, 10), no_scrollbar=True, key='-TEXT-')],
          [sg.Button("Cancel", key='OK')]]


def countdown(min, sec):
    global wpm
    timer = datetime.timedelta(seconds=sec, minutes=min)
    while timer.seconds > 0:
        time.sleep(1)
        timer -= datetime.timedelta(seconds=1)
        window["-TIMER-"].Update(str(timer))
        if timer.seconds == 0:
            wpm = len(completed_words) - missed_words
            print(len(completed_words))
            sg.popup_ok(f'Here are your results: {wpm}/WPM', title="Time's up!")
    window["-TIMER-"].Update("0:00:00")
    time.sleep(1)
    return 0


window = sg.Window("Speed Typing Test", layout, element_justification='center',
                   return_keyboard_events=True, use_default_focus=False)

words = []


def random_word_gen():
    with open('words') as f:
        data = f.readlines()
        random_words = random.choices(data, k=EASY_WORD_COUNT)
        random_words = [random_word.strip() for random_word in random_words]
        words.append(random_words)
    return random_words


do_not_listen = ['BackSpace:8', 'Tab:9', 'Return:13', 'Shift:16', 'Control_L:17', 'Alt:18', 'PauseBreak:19',
                 'Caps_Lock:20', 'Shift_L:16', 'Alt_L:18', 'Alt_R:18', 'Win_L:91', 'Down:40', 'Right:39', 'Left:37',
                 'Up:38', 'MouseWheel:Up', 'MouseWheel:Down', 'Escape:27', '__TIMEOUT__']

completed_words = []
missed_words = 0
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
        if event not in do_not_listen and event not in completed_words:
            text_elem.update(value=str(event)[0])
    if ord(str(event)[0]) == 32:
        if values['-TEXT-'].lower() == 'start':
            thread_timer = threading.Thread(target=countdown, args=(minutes, seconds), daemon=True).start()
            text_elem.update(value='')
            window['-WORDS-'].update(random_word_gen())
        else:
            completed_words.append(values['-TEXT-'].split(' '))
            text_elem.update(value='')
            window['-WORDS-'].update(f'Last word: {completed_words[-1]}\nNew Word: {random_word_gen()}')
            for word in completed_words:
                if word in words:
                    window['-WORDS-'].update(text_color='green')
                else:
                    missed_words += 1
                    window['-WORDS-'].update(text_color='red')

window.close()
