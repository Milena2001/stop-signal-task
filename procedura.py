from psychopy import visual, core, event
import random
import csv

N_TRIALS_TRAIN = 1
N_TRAILS_EXP = 4
REACTION_KEYS = ['left', 'right']
RESULTS = [["NR", "EXPERIMENT", "ACC", "RT", "TRIAL_TYPE", "REACTION"]]


def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=keys)
    return key[0]


def show_text(win, info, wait_key=["space"]):
    info.draw()
    win.flip()
    reactions(wait_key)

def part_of_experiment(n_trials, exp, fix):
    for i in range(n_trials):
        stim_type = random.choice(list(stim.keys()))
        stim[stim_type].setAutoDraw(True)
        window.callOnFlip(clock.reset)
        window.flip()
        key = reactions(REACTION_KEYS)
        rt = clock.getTime()
        stim[stim_type].setAutoDraw(False)
        window.flip()
        acc = stim_type == key
        RESULTS.append([i+1, exp, acc, rt, stim_type, key])


window = visual.Window(units="pix", color="gray", fullscr=False)
window.setMouseVisible(False)

clock = core.Clock()

arrowVert = [(-0.4,0.05),(-0.4,-0.05),(-.2,-0.05),(-.2,-0.1),(0,0),(-.2,0.1),(-.2,0.05)]
arrow = ShapeStim(win, vertices=arrowVert, fillColor='darkred', size=.5, lineColor='red')

fix = visual.TextStim(win=window, text="+", height=40)

inst1 = visual.TextStim(win=window, text="instrukcja", height=20)
inst2 = visual.TextStim(win=window, text="teraz eksperyment", height=20)
inst_end = visual.TextStim(win=window, text="koniec", height=20)


# TRAINING
show_text(win=window, info=inst1)
part_of_experiment(N_TRIALS_TRAIN, exp=False, fix=fix)

# EXPERIMENT
show_text(win=window, info=inst2)
part_of_experiment(N_TRAILS_EXP, exp=True, fix=fix)

# THE END
show_text(win=window, info=inst_end)

with open("result.csv", "w", newline='') as f:
    write = csv.writer(f)
    write.writerows(RESULTS)


