##########################
#### Import functions ####
##########################

import os # for path functions
from psychopy import visual, monitors, event, core    # type: ignore
from random import sample, shuffle
from shutil import move

###########################
#### Define functions ####
##########################

def code_generator(msg):
    chars = []
    visual.TextStim(win, msg, pos=(0, -200)).draw()
    win.flip()
    while True:
        key = event.waitKeys()[0].lower()
        if key == "return":
            if len(chars) == 6:
                break
        elif key in "abcdefghijklmnopqrstuvwxyz0123456789":
            if len(chars)<6:
                chars.append(key)
        elif key == "backspace":
            chars = chars[:-1]
        code="".join(chars)
        visual.TextStim(win, code.upper()).draw()
        visual.TextStim(win, msg, pos=(0, -200)).draw()
        win.flip()
    win.flip()
    return code

def show_text(text):
    visual.TextStim(win, text, pos = (0,0)).draw() # Vorbereitung Anzeige Instruktionen, #Vorbereitung auf Darstellung
    win.flip() #Übergang zur Anzeige Instruktionen, #Anzeige, win weil unser Fenster so heißt; flip ist der Befehl, um das gedrawte auf win zu setzen
    event.waitKeys(keyList = ["return"]) #Warten auf Knopfdruck
    win.flip()
    core.wait(2)

def prepare_text(text):
    visual.TextStim(win, text, pos = (0,0)).draw() # Vorbereitung Anzeige Instruktionen, #Vorbereitung auf Darstellung


def fixation_phase():
    fixation = visual.Circle(win, size = 5,lineColor = 'white', fillColor = 'lightGrey').draw()
    win.flip()
    core.wait(1)


def practice(stim, dict_key, condition):
    fixation_phase()
    if "st" in dict_key:
        imgzoomin = visual.ImageStim(win, image = stim, pos = (0, 0), size = (1400,970))
        imgzoomout = visual.ImageStim(win, image = stim, pos = (0, 0), size = (1000,630))
        img = visual.ImageStim(win, image = stim, pos = (0, 0), size = (1200, 800))
    if "ti" in dict_key:
        imgzoomin = visual.ImageStim(win, ori = 10, image = stim, pos = (0, 0), size = (1400,970))
        imgzoomout = visual.ImageStim(win, ori = 10, image = stim, pos = (0, 0), size = (1000,630))
        img = visual.ImageStim(win, ori = 10, image = stim, pos = (0, 0), size = (1200, 800))
    img.draw()
    win.flip()
    key, rt = event.waitKeys(timeStamped = clock, keyList=("w","s"))[0]
    if key == "w":
        imgzoomin.draw()
    if key == "s":
        imgzoomout.draw()
    win.flip()
    event.waitKeys(keyList=("return"))
    if condition == "straightapproach":
        if (key == "w" and "st" in dict_key) or (key =="s" and "ti" in dict_key):
            prepare_text(text = feedback.format("korrekt"))
        else:
            prepare_text(text = feedback.format("nicht korrekt"))
    else:
        if (key == "w" and "st" in dict_key) or (key =="s" and "ti" in dict_key):
            prepare_text(text = feedback.format("nicht korrekt"))
        else:
            prepare_text(text = feedback.format("korrekt"))
    win.flip()
    event.waitKeys(keyList=("return"), maxWait = 4)


def trial(stim, reference_dict_key, condition):
    fixation_phase()
    if "st" in reference_dict_key:
        imgzoomin = visual.ImageStim(win, image = stim, pos = (0, 0), size = (1400,970))
        imgzoomout = visual.ImageStim(win, image = stim, pos = (0, 0), size = (1000,630))
        img = visual.ImageStim(win, image = stim, pos = (0, 0), size = (1200, 800))
    if "ti" in reference_dict_key:
        imgzoomin = visual.ImageStim(win, ori = 10, image = stim, pos = (0, 0), size = (1400,970))
        imgzoomout = visual.ImageStim(win, ori = 10, image = stim, pos = (0, 0), size = (1000,630))
        img = visual.ImageStim(win, ori = 10, image = stim, pos = (0, 0), size = (1200, 800))
    img.draw()
    win.callOnFlip(clock.reset)#should work?
    win.flip()
    key, rt = event.waitKeys(timeStamped = clock, keyList=("w","s"))[0]
    if key == "w":
        imgzoomin.draw()
    if key == "s":
        imgzoomout.draw()
    win.flip()
    with open(filename, "a") as f:
        print(reference_dict_key,stim,key,rt,condition,subject_ID, sep=",", file=f)
    event.waitKeys(keyList=("return"), maxWait = 4)


#######################
#### Text elements ####
#######################

welcome = """Willkommen zu unserem Experiment!
Hierbei geht es um die Annäherung oder das Entfernen von visuellen Stimuli.
Das Experiment ist in zwei Durchgänge aufgeteilt, durch die Sie vom Programm geführt werden.

Drücken Sie ENTER um fortzufahren...
"""

code_generation = """
An dieser Stelle gibt die Versuchsleitung den
anonymisierten Proband:innen Code ein.
"""

feedback = """
Die gegebene Antwort war {}!

Drücken Sie ENTER, um fortzufahren...
"""

approach_practice = """
Im Folgendenen werden ihnen Trainingsdurchgänge präsentiert.
Wenn das Bild {} ist, sollen Sie sich annähern.
Dies erreichen Sie durch Drücken der Taste W.
Wenn das Bild hingegen {} ist, sollen Sie sich entfernen.
Dies erreichen Sie durch Drücken der Taste S.
Antworten Sie so schnell und genau wie möglich. Sowohl die Korrrektheit als auch die Reaktionszeit werden gemessen.
In den Trainingsdurchgängen erhalten Sie Feedback zu Ihrer Antwort.
Mit ENTER können Sie Text weiterschalten.

Drücken Sie ENTER um fortzufahren...
"""

approach_trials = """
Die Trainingsdurchgänge sind geschafft. Nun geht es in die Testphase.
Denken Sie daran, dass sie gelernt haben, dass sie sich annähern sollen, wenn das Bild {} ist.
Dies erreichen Sie durch Drücken der Taste W.
Wenn das Bild hingegen {} ist, sollen Sie sich entfernen.
Dies erreichen Sie durch Drücken der Taste S.
Sie werden in dieser Phase kein Feedback zu Ihren Antworten erhalten. Das nächste Bild wird also automatisch erscheinen!

Drücken Sie ENTER um fortzufahren...
"""

goodbye = """Der zweite Durchgang ist abgeschlossen!
Vielen Dank für Ihre Teilnahme. Beenden Sie das Programm und informieren Sie die Versuchsleitung.

Drücken Sie ENTER zum Beenden...
"""

#######################
#### Text elements ####
#######################

os.chdir('./stimuli')


neg_image_array = []
neutral_image_array = []
practice_image_array = []

for i in range(1,7):
    practice_image_array.append("practice" + str(i)+ ".jpg")

for i in range(1,7):
    neg_image_array.append("internet" + str(i)+ ".jpg")
    neutral_image_array.append("neutral" + str(i)+ ".jpg")

tilt_practice = sample(practice_image_array, 3)
straight_practice = list(set(practice_image_array).difference(tilt_practice))

tilt = sample(neutral_image_array, 3)
tilt.extend(sample(neg_image_array, 3))
straight = list(set(neutral_image_array).difference(tilt))
straight.extend(set(neg_image_array).difference(tilt))

practice_dict = {}
for i in range (0,3):
  practice_dict_key = "st" + str(i+1)
  practice_dict[practice_dict_key] = straight_practice[i]
for i in range (0,3):
  practice_dict_key = "ti" + str(i+1)
  practice_dict[practice_dict_key] = tilt_practice[i]

practice_order = list(iter(practice_dict))
shuffle(practice_order)

reference_dict = {}
for i in range (0,6):
  reference_dict_key = "st" + str(i+1)
  reference_dict[reference_dict_key] = straight[i]
for i in range (0,6):
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


##-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
##-#-#-# START EXPERIMENTAL PROCEDURE  #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
##-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

conditions = ["straightapproach", "tiltapproach"]
shuffle(conditions)

show_text(welcome)

subject_ID = code_generator(msg = code_generation)

if conditions[0] == "straightapproach":
        show_text(text = approach_practice.format("gerade", "schief"))
else:
        show_text(text = approach_practice.format("schief", "gerade"))

for single_stim in practice_order:
    practice(stim = practice_dict.get(single_stim), dict_key = single_stim,
            condition = conditions[0])

filename = "subject_" + subject_ID + ".csv"
with open(filename, "w") as f:
    print("alignment,stim_name,pressed_key,rt,align_condition,subject_ID", file = f)

if conditions[0] == "straightapproach":
        show_text(text = approach_trials.format("gerade", "schief"))
else:
        show_text(text = approach_trials.format("schief", "gerade"))

for single_stim in stimuli_order:
    trial(stim = reference_dict.get(single_stim), reference_dict_key = single_stim,
    condition = conditions[0])


origin = "subject_" + subject_ID + ".csv"
destination = ("../data")
move(origin, destination)

show_text(goodbye)

win.close()
core.quit()
