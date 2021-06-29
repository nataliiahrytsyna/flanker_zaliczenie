import psychopy.event
from psychopy import event, visual, core
import random
import csv
import yaml

from instructions import instructions
instructions = instructions

# timer setup
clock = core.Clock()

# read vars from yaml file
conf = yaml.load(open('config.yaml', encoding='utf-8'))
data = conf['DATA']

def display_instructions():
    # generating instruction display
    def instruction(it, key, cooldown=0):
        instruct = visual.TextStim(win=window, text=instructions[it], pos=(0.0, 0.0))
        instruct.draw()
        psychopy.event.waitKeys(keyList=[key])
        window.flip()
        core.wait(cooldown)  # cooldown chroni przed przeskakiwaniem wielu okien

    welcome = visual.TextStim(win=window, text=instructions[0], pos=(0.0, 0.0))
    # holds the welcome screen until any key is pressed
    while True:
        welcome.draw()
        window.flip()
        if len(event.getKeys()) >= 0:  # condition is a pressed SPACE key
            break
        event.clearEvents()

    instruction(1, "space")
    instruction(2, "space")
    instruction(3, "space")
    psychopy.event.waitKeys(keyList=['t'])
    return

def interlude(training_nr):
    interluder = visual.TextStim(win=window, text=instructions[4] if training_nr == 1 else instructions[5] , pos=(0.0, 0.0))
    # holds the welcome screen until any key is pressed
    while True:
        interluder.draw()
        window.flip()
        if psychopy.event.waitKeys(keyList=["space"]):  # condition is a pressed SPACE key
            break
        return

# this runs the end screen
def end_task():
    bye = visual.TextStim(win=window, text="Task finished. Thank you! \n Press Q to quit.")
    running = True
    print(data)
    while running:
        bye.draw()
        window.flip()
        psychopy.event.waitKeys(keyList=["q"])
        running = False
    return

# Here we send th the func info about number of trials,
# type of stimuli, and boolean of training/experiment mode
def run_experiment(n_trials, is_congruent, is_experiment):

    for i in range(n_trials):
        arrow_direction = conf['ARROW_LIST'][random.randint(0, 1)]
        flanker_direction = conf['ARROW_LIST'][random.randint(0, 1)]

        # setup coordinates of the red flanker arrow
        flanker_pos = (width_list[random.randrange(len(width_list))],height_list[random.randrange(len(height_list))])

        if is_congruent:
            flanker_direction = arrow_direction

        # drawing fixation point
        fix = visual.TextStim(win=window, text="+", height=40)
        fix.draw()
        window.flip()
        core.wait(0.8)

        # creating gray background arrows
        for j in range(100):
            arrow_pos=(width_list[random.randrange(len(width_list))], height_list[random.randrange(len(height_list))])

            # comparing positions of flanker and bg arrows. They shouldn't be in one place
            while flanker_pos == arrow_pos:
                arrow_pos = (width_list[random.randrange(len(width_list))], height_list[random.randrange(len(height_list))])

            arrow = visual.TextStim(win=window,
                                  text=arrow_direction,
                                  height=40,
                                  color="black",
                                  pos=arrow_pos)

            arrow.draw()

        flanker = visual.TextStim(win=window, text=flanker_direction, height=40, color="#d50000", pos=flanker_pos)
        flanker.draw()
        window.callOnFlip(clock.reset)
        window.flip()

        # determine what keyboard's key has the user used
        current_key = event.waitKeys(maxWait=1, keyList=["left", "right", "q"])
        key = 0
        if current_key != None:
            if current_key[0] == 'left' and flanker_direction == "<":
                key = 1
            elif current_key[0] == 'right' and flanker_direction == ">":
                key = 1
            elif current_key[0] == "q":
                core.quit()

        rt = clock.getTime()
        data.append([i+1, is_experiment, rt, is_congruent, key])

# Setting up experiment's window size
window = visual.Window(units="pix", color="gray", fullscr=True)

# Saving half-size of the monitor to a var,
# we need it for setting up limits of arrow spawning
monitor = window.size//2

# 2 arrays with width and height coordinates. The step of arrows appearing is 20 pix.
# Also they will not appear the first and last 20 pix of the screen.
width_list = []
for i in range(-(monitor[0])+20, monitor[0]-20, 20):
    width_list.append(i)

height_list = []
for i in range(-(monitor[1])+20, monitor[1]-20, 20):
    height_list.append(i)

# INSTRUCTIONS
display_instructions()

# TRAINING
run_experiment(conf['N_TRIALS_TRAINING'], True, False)
interlude(training_nr=1)
run_experiment( conf['N_TRIALS_TRAINING'], False, False)
interlude(training_nr=2)

# EXPERIMENT
run_experiment(conf['N_TRIALS'], False, True)

#COFFEE BREAK
break_text = visual.TextStim(win=window, text=instructions[6], pos=(0.0, 0.0))
break_text.draw()
window.flip()
core.wait(conf['BREAKTIME'])

# THE SECOND PART OF EXPERIMENT
run_experiment(conf['N_TRIALS'], False, True)

# save data from array to file
with open("flanker_task_results.csv", "w", newline="") as f:
    write = csv.writer(f)
    write.writerows(data)

# Show the last screen
end_task()
