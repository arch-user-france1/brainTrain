#!/bin/python
import os
import sys
import time
import iostream
import termcolor
from time import sleep
import random
#import gi

#gi.require_version('Gtk', '3.0')
#from gi.repository import Gtk

#win = Gtk.Window()
#win.connect("destroy", Gtk.main_quit)
#win.show()
#Gtk.main()

try:
    mode = sys.argv[1]
except IndexError:
    print("argument 1 is missing:\n"
          "argument 1: mode - train, new, loadarray, textfile")
    sys.exit(1)

iostr = iostream.iostream()
cards = iostr.openDictionary('cards', create=True)


def save_exit(status=0, save_set=False, setName=None, setData=None):
    if save_set:
        iostr.saveDictionary(setData, setName)
    iostr.saveDictionary(cards, 'cards')
    sys.exit(status)


def getArgument(argumentNr, usage, exitStatus=0):
    try:
        return sys.argv[argumentNr]
    except IndexError:
        print(f"argument {argumentNr} is missing\n"
              f"argument {argumentNr}: {usage}")
        sys.exit(exitStatus)


def setSetup(setName, set):
    try:
        if not cards[setName]:
            print("This set isn't configured yet, let's set it up.")
            options = []
            """
            options[0]: reliability 
            """
            print("How good do you want to be at the set?")
            answer = iostr.askFor(["bad", "medium", "good", "perfect"])
            if answer == "bad":
                options.append(40)
            elif answer == "medium":
                options.append(70)
            elif answer == "good":
                options.append(90)
            elif answer == "perfect":
                options.append(100)
            print("Ignore missing/too many whitespaces [yes/no]?")
            answer = iostr.askFor(["yes", 'y', "no", 'n'], firstAsk=False)
            if answer == "yes" or "y":
                options.append(True)
            else:
                options.append(False)
            print("setup completed")

            cards[setName] = {'options': options, 'cardData': {}, 'folders': []}
            for i in set:
                cards[setName]['cardData'][i] = [0, 0]  # correct answers, wrong answers
            print("\n")
            iostr.saveDictionary(cards, 'cards')
    except KeyError:
        pass


if mode == "train":

    def training(set, inLoop):
        if inLoop:
            enumMe = wrongAnswers
        else:
            enumMe = set
        for x, i in enumerate(enumMe):
            try:
                reliability = cards[setName]['cardData'][i][0] / (
                        cards[setName]['cardData'][i][0] + cards[setName]['cardData'][i][1]) * 100
            except ZeroDivisionError:
                reliability = 0
            if reliability <= cards[setName]['options'][0] and cards[setName]['cardData'][i][0] < 4:
                if not reversed_definitions:
                    print(x + 1, ". ", i, end="   ")
                else:
                    print(x + 1, ". ", set[i], end="   ")
                try:
                    answer = input()
                except UnicodeEncodeError:
                    print("UnicodeDecodeError :/   try using a different shell or submit a PR")
                    answer = ""

                if not reversed_definitions:
                    correct = iostr.checkAnswer(answer, set[i])
                else:
                    correct = iostr.checkAnswer(answer, i)

                if correct:
                    if not reversed_definitions:
                        print(termcolor.colored(set[i], "green"))
                    else:
                        print(termcolor.colored(i, "green"))
                    print("Correct!")
                    cards[setName]['cardData'][i][0] += 1
                    if inLoop:
                        wrongAnswers.remove(i)
                    sleep(0.3)
                else:
                    print("Correct answer would've been:")
                    if not reversed_definitions:
                        output = set[i]
                    else:
                        output = i

                    outputArr = list(output)
                    answerArr = list(answer)
                    difference = len(outputArr) - len(answerArr)
                    if difference != 0:
                        if difference < 0:
                            iterate = len(outputArr)
                            tooLong = "answer"
                        elif difference > 0:
                            iterate = len(answerArr)
                            tooLong = "output"
                    else:
                        tooLong = ''
                        iterate = len(answerArr)

                    for n in range(iterate):
                        if outputArr[n] == answerArr[n]:
                            print(termcolor.colored(answerArr[n], 'green'), end="")
                        else:
                            print(termcolor.colored(outputArr[n], 'red'), end="")

                    if tooLong == "anwer":
                        for m in range(len(answerArr) - iterate):
                            idx = m + iterate
                            print(termcolor.colored(outputArr[idx], 'red'), end="")
                        del idx, m
                    elif tooLong == "output":
                        for m in range(len(outputArr) - iterate):
                            idx = m + iterate
                            print(termcolor.colored(outputArr[idx], 'blue'), end="")

                        del idx, m
                    del iterate, n, difference, outputArr, output, answerArr

                    print('\n'
                        f"Press {termcolor.colored('enter', 'red')} to continue, type {termcolor.colored('correct', 'green')} if it was correct")
                    correct = input()
                    if correct == "correct":
                        print(f"You typed {termcolor.colored('correct', 'green')}\n")
                        cards[setName]['cardData'][i][0] += 1
                        if inLoop:
                            wrongAnswers.remove(i)
                    else:
                        print()
                        #print("You didn't type correct\n")
                        cards[setName]['cardData'][i][1] += 1
                        if not inLoop:
                            wrongAnswers.append(i)



    setName = getArgument(2, "the name of the set")
    error = 0

    set = iostr.openDictionary(setName)
    if set is None:
        print("Couldn't load that set!")
        sys.exit(1)
    reversed_definitions = False
    try:
        if sys.argv[3] or sys.argv[3] == "reversed":
            reversed_definitions = True
    except:
        pass

    setSetup(setName, set)

    cards[setName]["lastAccessed"] = time.time()
    try:
        wrongAnswers = []
        set = iostr.shuffleDictionary(set)
        training(set, inLoop=False)

        running = True
        while running:
            if len(wrongAnswers) > 0:
                random.shuffle(wrongAnswers)
                os.system("clear 2>/dev/zero")
                training(set, inLoop=True)
                sleep(0.5)
            else:
                running = False

        save_exit(save_set=False)
        print("Your progress has been saved.")

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt exception has occurred! Saving progress..")
        save_exit(save_set=False)
        print("Your progress has been saved.")
        sys.exit(1)

if mode == "new":
    print("Title")
    set = input()
    words = iostr.addWords()
    cards[set] = False
    iostr.saveDictionary(dictionary=words, fileName=set)
    iostr.saveDictionary(cards, 'cards')
    print("Your new set has been saved.")

elif mode.lower() == "loadarray":
    f = open(sys.argv[2])
    array = eval(f.read())
    last = False
    words = {}
    x = 0
    for i in array:
        if not last:
            last = i
            x += 1
        else:
            words[last] = i
            last = False
    print("The array has been converted into a dictionary:")
    print(words)
    # print("How shall the set be called?   ", end="")
    set = input("How shall the set be called?    ")
    print(f"Saving the new set which has {x} definitions under the name {set}...")
    cards[set] = False
    save_exit(0, True, set)
    print("done")

elif mode.lower() == "textfile":
    last = False
    words = {}
    x = 0
    with open(sys.argv[2]) as f:
        for i in f:
            i = i.rstrip()
            if not last:
                last = i
                x += 1
            else:
                words[last] = i
                last = False
        print("The list has been converted into a dictionary:")
        print(words)
        print("How shall the set be called?   ", end="")
        set = input()
        print(f"Saving the new set which has {x} definitions under the name {set}...")
        cards[set] = False
        save_exit(0, True, setName=set, setData=words)

elif mode.lower() == "resetset":
    print(
        f"Do you really want to delete your configuration for the set {getArgument(2, 'the name of the set')} and reset your training data?")
    if input("Yes: [Y y] / No: anything else\n").lower() == "y":
        print("You answered yes")
        cards[getArgument(2, "the name of the set")] = False
        save_exit()
    else:
        print("You didn't answer y. Your configuration won't be deleted.")
        save_exit(1)

elif mode == "list":
    print("-----------SETS-----------")
    sets = {}
    for i in cards:
        try:
            lastAccessed = cards[i]["lastAccessed"]
            sets[lastAccessed] = i
        except:
            print(f"Warning: invalid set {i}")
    sortedSets = sorted(sets, reverse=True)

    for output in sortedSets:
        output = sets[output]
        nameLength = len(output)
        if nameLength > 27:
            outputArr = output.split()
            output = ""
            for j,x in enumerate(outputArr):
                if j < 27:
                    output += x
                else:
                    break
            output += "..."
            nameLength = len(output)

        spaces = 32 - nameLength

        print(termcolor.colored(output, "blue"), end="")
        for j in range(spaces):
            print(end=" ")
        print(termcolor.colored(time.ctime(cards[i]['lastAccessed']), "green"))

elif mode == "folders":
    folders = iostr.openDictionary("folders")


    def list_folders():
        folderName = getArgument(3, "the name of the new folder")
        print("-----------SETS-----------")
        sets = {}
        for i in folders[folderName]:
            lastAccessed = cards[i]["lastAccessed"]
            sets[lastAccessed] = i
        sortedSets = sorted(sets, reverse=True)

        for output in sortedSets:
            print(termcolor.colored(sets[output], "blue"), "             ",
                  termcolor.colored(time.ctime(output), "green"))


    if len(sys.argv) == 3:
        list_folders()

    mode = getArgument(2, "new, add, list")

    if mode == "create" or mode == "new":
        folderName = getArgument(3, "the name of the new folder")
        folders = iostr.openDictionary('folders', True)
        folders[folderName] = []
        iostr.saveDictionary(folders, "folders")
        print(f"Folder {folderName} has been created")
        sys.exit(0)

    elif mode == "add":
        folderName = getArgument(4, "the name of the folder")
        setName = getArgument(3, "the name of the set")
        setSetup(setName, set=iostr.openDictionary(setName))
        print(f"adding {setName} to your folder {folderName}...")
        if folderName in cards[setName]['folders']:
            print("That set is already in that folder. Won't add it.")
            sys.exit(1)
        cards[setName]['folders'].append(folderName)

        if folders is None:
            print("The file folders.json is not existing. Please first create a folder and then add a set to it.")
            sys.exit(1)
        try:
            if setName not in folders[folderName]:
                folders[folderName].append(setName)
        except KeyError:
            print(f"That folder doesn't exist. Please first create it: ./main.py folders create {folderName}")
            cards[setName]['folders'].remove(folderName)
            sys.exit(1)

        iostr.saveDictionary(folders, 'folders')
        iostr.saveDictionary(cards, 'cards')
        print(f"Your set {setName} has been added to the folder {folderName}.")
        sleep(0.2)
        list_folders()
        sys.exit(0)

    elif mode == "list":
        list_folders()
