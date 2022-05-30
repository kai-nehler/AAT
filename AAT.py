##########################
#### Import functions ####
##########################

import os                                             # for path functions
from shutil import move                               # for path function
from psychopy import visual, monitors, event, core    # type: ignore # important functions for conducting experiments
from random import sample, shuffle                    # randomize conditions and stimuli


###########################
#### Define functions ####
##########################

def show_text(text):
    visual.TextStim(win, text, pos = (0,0)).draw()  # Preperation of a text stimuli
    win.flip()                                      # start presentation - win is a name of screen; flip brings drawn stimuli onto the screen
    event.waitKeys(keyList = ["return"])
    win.flip()                                      # empty frame for buffer after confirming
    core.wait(0.8)                                  # time for buffer

def code_generator(msg):
    chars = []
    visual.TextStim(win, msg, pos=(0, -200)).draw()
    win.flip()
    while True:                                                 # loop stays always TRUE - must escape via break
        key = event.waitKeys()[0].lower()
        if key == "return":
            if len(chars) == 6:                                 # enter only breaks, if code is complete
                break
        elif key in "abcdefghijklmnopqrstuvwxyz0123456789":
            if len(chars)<6:
                chars.append(key)
        elif key == "backspace":
            chars = chars[:-1]
        code="".join(chars)
        visual.TextStim(win, code.upper()).draw()               # redraw text stimuli to show user input on frame
        visual.TextStim(win, msg, pos=(0, -200)).draw()
        win.flip()
    win.flip()
    return code

def fixation_preparation_phase(stim, dict_key):
    fixation = visual.Circle(win, size = 5,lineColor = 'white', fillColor = 'lightGrey').draw()
    win.flip()  # Show prepared fixation object
    clock.reset()
    #clock_two.reset() #Timing Testing
    if "st" in dict_key:
        imgzoomin = visual.ImageStim(win, image = stim, pos = (0, 0), size = (875,606.25))
        imgzoomout = visual.ImageStim(win, image = stim, pos = (0, 0), size = (450,283.5))
        img = visual.ImageStim(win, image = stim, pos = (0, 0), size = (600, 400))
        img.draw()
    if "ti" in dict_key:
        imgzoomin = visual.ImageStim(win, ori = 2, image = stim, pos = (0, 0), size = (875,606.25))
        imgzoomout = visual.ImageStim(win, ori = 2, image = stim, pos = (0, 0), size = (450,283.5))
        img = visual.ImageStim(win, ori = 2, image = stim, pos = (0, 0), size = (600, 400))
        img.draw()
    while True:                         # check timing after preperation of stimulie
        if clock.getTime() <= 1.5:      # preperation should take less than this time
            pass
        else:
            break
    return img, imgzoomin, imgzoomout


def practice(stim, dict_key, condition):
    img, imgzoomin, imgzoomout = fixation_preparation_phase(stim = stim, dict_key = dict_key)
    #print(clock_two.getTime()) # timing check
    win.flip()
    #print(clock_two.getTime())  #timing check
    key, rt = event.waitKeys(timeStamped = clock, keyList=("up","down"))[0]
    if key == "up":
        imgzoomin.draw()
    if key == "down":
        imgzoomout.draw()
    win.flip()
    event.waitKeys(keyList=("return"), maxWait = 1.5)
    if condition == "straightapproach":
        if (key == "up" and "st" in dict_key) or (key =="down" and "ti" in dict_key):
            show_text(text = feedback.format("korrekt"))
        else:
            show_text(text = feedback.format("nicht korrekt"))
    else:
        if (key == "up" and "st" in dict_key) or (key =="down" and "ti" in dict_key):
            show_text(text = feedback.format("nicht korrekt"))
        else:
            show_text(text = feedback.format("korrekt"))


def trial(stim, dict_key, condition):
    img, imgzoomin, imgzoomout = fixation_preparation_phase(stim = stim, dict_key = dict_key)
    #print(clock_two.getTime()) # timing check
    win.callOnFlip(clock.reset)
    win.flip()
    #print(clock.getTime()) # timing check
    #print(clock_two.getTime()) # timing check
    key, rt = event.waitKeys(timeStamped = clock, keyList=("up","down"))[0]
    #print(clock.getTime()) # timing check
    if key == "up":
        imgzoomin.draw()
    if key == "down":
        imgzoomout.draw()
    win.flip()
    with open(filename, "a") as f:
        print(dict_key,stim,key,rt,condition,subject_ID, sep=",", file=f)
    event.waitKeys(keyList=("return"), maxWait = 1.5)


#######################
#### TEXT ELEMENTS ####
#######################

welcome = """Willkommen!
In diesem Experiment geht es darum, sich auf Bilder zu oder von ihnen weg zu bewegen.
Das Experiment ist in zwei Durchgänge aufgeteilt, durch die du vom Programm geführt wirst.

Drücke ENTER, um fortzufahren...
"""

code_generation = """
An dieser Stelle gibt die Versuchsleitung den
anonymisierten Proband:innen Code ein.
"""

double = """
Eine Datei mit diesem Code liegt bereits vor. Bitte geben Sie einen einzigartigen Code ein.

Drücke ENTER, um einen neuen Code einzugeben...
"""

feedback = """
Die gegebene Antwort war {}!

Drücke ENTER, um fortzufahren...
"""

approach_practice = """
Im Folgendenen werden Trainingsdurchgänge präsentiert.

Wenn das Bild {} ist, sollst du auf das Bild zugehen. Das erreichst du durch die Pfeiltaste nach oben. Wenn das Bild hingegen {} ist, sollst du dich von dem Bild weg bewegen. Das erreichst mit der Pfeiltaste nach unten.

Antworte bitte so schnell und genau wie möglich. Sowohl die Korrrektheit als auch die Reaktionszeit werden gemessen. In den Trainingsdurchgängen gibt es Feedback zur Reaktion, in den eigentlichen Durchgängen aber nicht mehr.


Drücke ENTER, um zu beginnen...
"""

approach_trials = """
Die Trainingsdurchgänge sind geschafft. Nun geht es in die Testphase.

Bitte denk daran, dass du dich auf das Bild zu bewegen sollst, wenn das Bild {} ist. Das machst du mit der Pfeiltaste nach oben. 

Wenn das Bild hingegen {} ist, sollst du dich vom Bild weg bewegen. Das geht mit der Pfeiltaste nach unten.

In dieser Phase wird es kein Feedback geben - das nächste Bild wird also automatisch erscheinen!

Drücke ENTER, um zu beginnen...
"""

intermediate = """
Der erste Durchgang ist geschafft. Nimm dir einen Moment Zeit und einen Schluck Wasser.

Wenn du bereit bist, starte in den zweiten Durchgang - zunächst wieder mit einem Probedurchlauf.

Drücke ENTER, um fortzufahren...
"""

goodbye = """Der zweite Durchgang ist abgeschlossen!
Vielen Dank für die Teilnahme! Beende das Programm und sage der Versuchsleitung Bescheid.

Drücke ENTER zum Beenden...
"""

####################################################################
#### RANDOMIZE PRACTICE AND TRIAL IMAGES TO BE TILT OR STRAIGHT ####
####################################################################

os.chdir('./stimuli')


neg_image_array = []
neutral_image_array = []
practice_image_array = []

for i in range(1,8):
    practice_image_array.append("practice" + str(i)+ ".jpg")

for i in range(1,25):
    neg_image_array.append("internet" + str(i)+ ".jpg")
    neutral_image_array.append("neutral" + str(i)+ ".jpg")

tilt_practice = sample(practice_image_array, 3)
straight_practice = list(set(practice_image_array).difference(tilt_practice))

tilt = sample(neutral_image_array, 12)
tilt.extend(sample(neg_image_array, 12))
straight = list(set(neutral_image_array).difference(tilt))
straight.extend(set(neg_image_array).difference(tilt))

practice_dict = {}
for i in range (0,4):
  practice_dict_key = "st" + str(i+1)
  practice_dict[practice_dict_key] = straight_practice[i]
for i in range (0,3):
  practice_dict_key = "ti" + str(i+1)
  practice_dict[practice_dict_key] = tilt_practice[i]

practice_order = list(iter(practice_dict))
shuffle(practice_order)

reference_dict = {}
for i in range (0,24):
  reference_dict_key = "st" + str(i+1)
  reference_dict[reference_dict_key] = straight[i]
for i in range (0,24):
  reference_dict_key = "ti" + str(i+1)
  reference_dict[reference_dict_key] = tilt[i]

stimuli_order = list(iter(reference_dict))
shuffle(stimuli_order)


#################################
#### Define monitor, window and clock ####
#################################
m = monitors.Monitor("test", width=28.8, distance=90, autoLog=True)
win = visual.Window(size = (1024,800),monitor=m, units='pix', winType='pyglet', color=-.5,fullscr=True) #Window Attribut aus visual aus psychopy erstellt hier ein Window, das zur Darstellung benutzt wird mit dem Objektnamen win
clock = core.Clock() #stopwatch
#clock_two = core.Clock() # timing testing
event.globalKeys.add(key="escape", func=core.quit)

##-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
##-#-#-# START EXPERIMENTAL PROCEDURE  #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
##-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

#### DETERMINE ORDER, SHOW INSTRUCTIONS AND SET UP FILE ----

conditions = ["straightapproach", "tiltapproach"]
shuffle(conditions)                                                       # randomize order of condtions

show_text(welcome)


subject_ID = code_generator(msg = code_generation)


while True:
    if os.path.exists("../data/subject_" + subject_ID + ".csv"):
        show_text(double)
        subject_ID = code_generator(msg = code_generation)
    else:
        break

filename = "subject_" + subject_ID + ".csv"
with open(filename, "w") as f:                                                              # set up file for data
    print("alignment,stim_name,pressed_key,rt,align_condition,subject_ID", file = f)        # first row will function as header later

#### FIRST CONDITION ----

if conditions[0] == "straightapproach":
        show_text(text = approach_practice.format("gerade", "schief"))
else:
        show_text(text = approach_practice.format("schief", "gerade"))

for single_stim in practice_order:
    practice(stim = practice_dict.get(single_stim), dict_key = single_stim,
            condition = conditions[0])

if conditions[0] == "straightapproach":
        show_text(text = approach_trials.format("gerade", "schief"))
else:
        show_text(text = approach_trials.format("schief", "gerade"))

for single_stim in stimuli_order:
    trial(stim = reference_dict.get(single_stim), dict_key = single_stim,
    condition = conditions[0])

#### SECOND CONDITION ----

show_text(intermediate)

shuffle(practice_order)
shuffle(stimuli_order)

if conditions[1] == "straightapproach":
        show_text(text = approach_practice.format("gerade", "schief"))
else:
        show_text(text = approach_practice.format("schief", "gerade"))

for single_stim in practice_order:
    practice(stim = practice_dict.get(single_stim), dict_key = single_stim,
            condition = conditions[1])

if conditions[1] == "straightapproach":
        show_text(text = approach_trials.format("gerade", "schief"))
else:
        show_text(text = approach_trials.format("schief", "gerade"))

for single_stim in stimuli_order:
    trial(stim = reference_dict.get(single_stim), dict_key = single_stim,
    condition = conditions[1])

#### MOVE DATA AND END EXPERIMENT ----

origin = "subject_" + subject_ID + ".csv"
destination = ("../data")
move(origin, destination)

show_text(goodbye)

win.close()
core.quit()
