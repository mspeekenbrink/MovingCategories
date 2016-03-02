#!/usr/bin/env python

from psychopy import core, visual, gui, data, misc, event, sound
import time, random, math
import numpy as np

stimulusHeight = .4
responseOptions = [0,1]
featureOptions = [0,1]
random.shuffle(responseOptions)
random.shuffle(featureOptions)
resolution = (1600,900)
correctChoices = 0
choice = 0
external = True
maxTrials = 700
transferTrials = 24
currentTrial = 1
correctChoices = 0
nCorrect = 0
itiTime = 500
feedTime = 1000
optionBoxColor = '#FFFFFF'
optionBoxFillColor = '#CCCCCC'
optionBoxHighlight = '#FFFF00'
correctColor = '#00FF00'
wrongColor = '#FF000000'

correctSound = sound.SoundPygame(value='Correct.wav')
wrongSound = sound.SoundPygame(value='Incorrect.wav')

## stimuli
meanA = np.array([97.0,123.0])
meanB = np.array([123.0,97.0])
cov = np.array([[162.5,112.0],[112.0,162.5]])
stimuli = [np.random.multivariate_normal(meanA,cov,700),
           np.random.multivariate_normal(meanB,cov,700)]
thetas = [np.concatenate(([0.0]*200,np.linspace(0.0,0.7854,100),[0.7854]*200,np.linspace(0.7854,0.0,100),[0.0]*100)),
         np.concatenate(([0.7854]*200,np.linspace(0.7854,0.0,100),[0.0]*200,np.linspace(0.0,0.7854,100),[0.7854]*100))]
tcat = [0,1]*50
categories = []
for i in range(700/25):
    random.shuffle(tcat)
    categories += tcat

def rotation(X,theta):
    return np.dot(X - np.array([110,110]),np.array([[math.cos(theta),-1.0*math.sin(theta)],[math.sin(theta),math.cos(theta)]])) + np.array([110,110])


instructions1 = 'In this experiment you will need to classify visual patterns into two equally likely categories, labelled as A and B. '
instructions1 += 'The patterns are "grating patterns" which vary in angle (rotation) and frequency (density of lines).'

instructions2 = 'On each trial you will be presented with a grating pattern. Below the pattern you will see the two options (A and B). '
instructions2 += 'You can press "f" to select the option on the left (A), and "j" to select the option on the right (B). '
instructions2 += 'After making your classification, you will be informed of the actual category the pattern belongs to. '
instructions2 += 'When you made a correct classification, your selection will be coloured green and you\'ll hear a chime sound. When '
instructions2 += 'you made an incorrect classification, your selection will be coloured in red and you\'ll hear a buzzer sound.'

instructions3 = 'You will be asked to classify a total of 700 patterns. The relation between the patterns and categories '
instructions3 += 'is not perfect, so you will not be able to always give the '
instructions3 += 'correct classification. At first the task may be difficult, but your performance should increase with practice.\n\n'
instructions3 += 'Note that the relation between the patterns and the categories may change during the task, so you may have to change '
instructions3 += 'the way you classify the patterns to keep performing well.'

instructions4 = 'For each correct classification, you will be rewarded with 1 point. The two best performers will each be rewarded with '
instructions4 += 'a 20 pound gift voucher. '

instructions5 = 'If you have any questions, please ask the experimenter now. Otherwise you can press any key to start the task.'

continueText = 'Press any key to continue'

expInfo = {'subject':'test', 'condition':1, 'sex':['male','female'],'age':19}

expInfo['dateStr']= data.getDateStr() #add the current time
#present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Category Learing', fixed=['dateStr'],order=['subject','condition','dateStr','sex','age'])
if dlg.OK:
    misc.toFile('lastParams.pickle', expInfo)#save params to file for next time
else:
    core.quit()#the user hit cancel so exit
    
      
#make a text file to save data
fileName = 'Data/' + expInfo['subject'] + expInfo['dateStr']
condition = expInfo['condition']
if condition == 1:
    print 'condition 1 \n' + 'responseOptions = ' + str(responseOptions) + '; featureOptions = ' + str(featureOptions) + '\n'
    theta = thetas[1]
else:
    print 'condition 2 \n' + 'responseOptions = ' + str(responseOptions) + '; featureOptions = ' + str(featureOptions) + '\n'
    theta = thetas[0]

dataFile = open(fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'

dataFile.write('id = ' + str(expInfo['subject']) + '; sex = ' + expInfo['sex'] + '; age = ' + str(expInfo['age']) + '; condition = ' + str(condition) + '; responseOrder = ' + str(responseOptions[0]) + '_' + str(responseOptions[1]) + '; featureOrder = ' + str(featureOptions[0]) + '_' + str(featureOptions[1]) + '\n')

win = visual.Window(resolution,allowGUI=False, monitor='Dell 17Inch', units='norm')

def angle_fun(x):
    #return 15 + (x+1)*30
    return x #- 90.0

def freq_fun(x):
    # maps min (97 - 3*sqrt(162.5)) to 1.5 and max (123 + 3*sqrt(162.5)) to 18 cycles per stimulus
    return (0.1609913 * x - 7.95824)/(stimulusHeight*resolution[1])

#display instructions and wait
instructions = visual.TextStim(win, pos=[0,0],text='Press any key to start')
instructions.setHeight(.08)
cont = visual.TextStim(win, pos=[.98,-.98], text = 'Press any key to continue', alignHoriz = 'right', alignVert = 'bottom')
cont.setHeight(.05)
instructions.draw()
win.flip()

#pause until there's a keypress
event.waitKeys()
instructions.setText(instructions1)
instructions.draw()
cont.draw()
win.flip()#to show our newly drawn 'stimuli'
event.waitKeys()

instructions.setText(instructions2)
instructions.draw()
cont.draw()
win.flip()#to show our newly drawn 'stimuli'
event.waitKeys()

instructions.setText(instructions3)
instructions.draw()
cont.draw()
win.flip()#to show our newly drawn 'stimuli'
event.waitKeys()

instructions.setText(instructions4)
instructions.draw()
cont.draw()
win.flip()#to show our newly drawn 'stimuli'
event.waitKeys()

instructions.setText(instructions5)
instructions.draw()
cont.draw()
win.flip()#to show our newly drawn 'stimuli'
event.waitKeys()

# Task
feedClock = core.Clock()
responseClock = core.Clock()
stimulus = visual.GratingStim(win, tex='sin', sf=5,  size=[stimulusHeight*resolution[1],stimulusHeight*resolution[1]], pos=[0,.4*stimulusHeight*resolution[1]],mask='gauss', ori=0, units='pix',interpolate=True)
option1Box = visual.ShapeStim(win,lineWidth=3,lineColor=optionBoxColor,pos=[-.1*win.size[0],-.25*win.size[1]],vertices=((-50, -50), (-50, 50), (50, 50), (50,-50)),units='pix')
option2Box = visual.ShapeStim(win,lineWidth=3,lineColor=optionBoxColor,pos=[.1*win.size[0],-.25*win.size[1]],vertices=((-50, -50), (-50, 50), (50, 50), (50,-50)),units='pix')
option1Label = visual.TextStim(win,pos=[-.2,-.5], text = 'A')
option2Label = visual.TextStim(win,pos=[.2,-.5], text = 'B')
trialBox = visual.TextStim(win,pos=[-.95,.95], text = "trial: " + str(currentTrial),  alignHoriz = 'left', alignVert = 'top',height=.07)
correctBox = visual.TextStim(win,pos=[.95,.95], text = "correct: " + str(correctChoices),  alignHoriz = 'right', alignVert = 'top',height=.07)

dataFile.write('trial,x1,x2,y,response,time,correct\n')

trialsDone = False
while not trialsDone:
    option1Box.setLineColor(optionBoxColor)
    option1Box.setFillColor(optionBoxFillColor)
    option2Box.setLineColor(optionBoxColor)
    option2Box.setFillColor(optionBoxFillColor)
    trialBox.setText('trial: ' + str(currentTrial))

    # get stimulus
    y = categories[currentTrial-1]
    x = rotation(stimuli[y][currentTrial],theta[currentTrial])
    dataFile.write(str(currentTrial) + "," + str(x[0]) + "," + str(x[1]) + "," + str(y) + ",")
    # display stimulus
    stimulus.setOri(angle_fun(x[featureOptions[0]]))
    stimulus.setSF(freq_fun(x[featureOptions[1]]))
    stimulus.draw()
    option1Box.draw()
    option1Label.draw()
    option2Box.draw()
    option2Label.draw()
    trialBox.draw()
    correctBox.draw()
    win.flip()
    # wait for response
    responseGiven = False
    trialOK = False
    responseGiven = False
    responseClock.reset()
    event.clearEvents()
    while not trialOK:
        for key in event.getKeys():
            if key in ['f']:
                choice = responseOptions[0]
                responseGiven = True
                option1Box.setLineColor(optionBoxHighlight)
                option2Box.setLineColor(optionBoxColor)
                trialOK = True
                responseTime = responseClock.getTime()
                dataFile.write(str(choice) + "," + str(responseTime) + ",")
            elif key in ['j']:
                choice = responseOptions[1]
                responseGiven = True
                option1Box.setLineColor(optionBoxColor)
                option2Box.setLineColor(optionBoxHighlight)
                trialOK = True
                responseTime = responseClock.getTime()
                dataFile.write(str(choice) + "," + str(responseTime) + ",")
            if key in ['F9','escape']:
                print "stopping"
                dataFile.close()
                win.close()
                core.quit()
        stimulus.draw()
        option1Box.draw()
        option1Label.draw()
        option2Box.draw()
        option2Label.draw()
        trialBox.draw()
        correctBox.draw()
        win.flip()
    
    if y == choice:
        correctSound.play()
        correctChoices += 1
        correctBox.setText('correct: ' + str(correctChoices))
        dataFile.write("1\n" )
    else:
        wrongSound.play()
        dataFile.write("0\n")
        
    ## Feedback
    if responseOptions[0] == choice:
        if y == choice:
            option1Box.setFillColor(correctColor)
        else:
            option1Box.setFillColor(wrongColor)
    if responseOptions[1] == choice:
        if y == choice:
            option2Box.setFillColor(correctColor)
        else:
            option2Box.setFillColor(wrongColor)             
    
    stimulus.draw()
    option1Box.draw()
    option1Label.draw()
    option2Box.draw()
    option2Label.draw()
    trialBox.draw()
    correctBox.draw()
    win.flip()
    core.wait(feedTime/1000)


    if currentTrial < maxTrials:
        currentTrial += 1
    else:
        trialsDone = True

    
    # ITI
    win.flip()
    core.wait(itiTime/1000)
        
# the end
endtext = "This is the end of the experiment. Thank you for participating.\n \n"
endtext += "You have made a total of " + str(correctChoices) + " correct classifications. "
endtext += "\n\nPlease leave this screen as it is and inform the experimenter you have finished the experiment."
ending = False
instructions.setText(endtext)
instructions.draw()
win.flip()
    
while not ending:
    for key in event.getKeys():
        if key in ['escape']:
            ending = True

dataFile.close()
win.close()
core.quit()
