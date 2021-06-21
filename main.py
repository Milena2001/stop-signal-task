import atexit
import codecs
import csv
import random
from os.path import join
from statistics import mean

import yaml
from psychopy import visual, event, logging, gui, core

from itertools import combinations_with_replacement, product

N_TRIALS_TRAIN = 1
N_TRAILS_EXP = 2
REACTION_KEYS = ['left', 'right']
RESULTS = [["NR", "EXPERIMENT", "ACC", "RT", "TRIAL_TYPE", "REACTION"]]

def read_text_from_file(file_name, insert=''):
    """
    Method that read message from text file, and optionally add some
    dynamically generated info.
    :param file_name: Name of file to read
    :param insert:
    :return: message
    """
    if not isinstance(file_name, str):
        logging.error('Problem with file reading, filename must be a string')
        raise TypeError('file_name must be a string')
    msg = list()
    with codecs.open(file_name, encoding='utf-8', mode='r') as data_file:
        for line in data_file:
            if not line.startswith('#'):  # if not commented line
                if line.startswith('<--insert-->'):
                    if insert:
                        msg.append(insert)
                else:
                    msg.append(line)
    return ''.join(msg)

def abort_with_error(err):
    """
    Call if an error occured.
    """
    logging.critical(err)
    raise Exception(err)

def show_info(window, file_name, insert=''):
    """
    Clear way to show info message into screen.
    :param win:
    :return:
    """
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(window, color='black', text=msg,
                          height=20)
    msg.draw()
    window.flip()
    key = event.waitKeys(keyList=['f7', 'return', 'space', 'left', 'right'])
    if key == ['f7']:
        abort_with_error(
            'Experiment finished by user on info screen! F7 pressed.')
    window.flip()

def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=keys)
    return key[0]


# def show_text(win, info, wait_key=["space"]):
#     info.draw()
#     win.flip()
#     reactions(wait_key)


def part_of_experiment(n_trials, exp, fix):
    for i in range(n_trials):
        stim_type = random.choice(list(stim.keys()))
        circle_type = random.choice(list(circle.keys()))
        fix.draw()
        core.wait(1)
        window.flip()
        core.wait(1)
        circle[circle_type].setAutoDraw(True)
        window.flip()
        stim[stim_type].draw()
        window.callOnFlip(clock.reset)
        window.flip()
        key = reactions(REACTION_KEYS)
        rt = clock.getTime()
        stim[stim_type].setAutoDraw(False)
        window.flip()
        circle[circle_type].setAutoDraw(False)
        window.flip()
        acc = stim_type == key
        RESULTS.append([i+1, exp, acc, rt, stim_type, key])

delay =

window = visual.Window(units="pix", color="gray", fullscr=True)
window.setMouseVisible(True)
mouse= event.Mouse (visible = True)

clock = core.Clock()

stim = {"left": visual.TextStim(win=window, text="←", height=120,bold=True, pos=(0,3)),
        "right": visual.TextStim(win=window, text="→", height=120, bold=True, pos=(0,3))}
#circle= visual.Circle(window, size=(120, 120), pos=(0,0), lineColor = 'white', fillColor = None)
circle= {"GO": visual.Circle(window, size=(130, 130), pos=(0,-8), lineColor = 'white', fillColor = None),
         "NO GO": visual.Circle(window, size=(130, 130), pos=(0,-8), lineColor = '#bf1616', fillColor = None)}

fix = visual.TextStim(win=window, text="+", height=80)


#inst1 = visual.TextStim(win=window, text="instrukcja", height=20)
#inst2 = visual.TextStim(win=window, text="teraz eksperyment", height=20)
#inst_end = visual.TextStim(win=window, text="koniec", height=20)

#POCZĄTKOWE INFORMACJE
show_info(window, 'instrukcja ogólna.txt', insert ='')

# TRAINING
show_info(window,'trening.txt', insert='')
part_of_experiment(N_TRIALS_TRAIN, exp=False, fix=fix)

# EXPERIMENT
show_info(window, 'czesc eksperymentalna.txt', insert='')
part_of_experiment(N_TRAILS_EXP, exp=True, fix=fix)
show_info(window,'trening.txt', insert='')
part_of_experiment(N_TRAILS_EXP, exp=True, fix=fix)
# THE END
show_info(window,'instrukcja.txt', insert='')

with open("result.csv", "w", newline='') as f:
    write = csv.writer(f)
    write.writerows(RESULTS)


