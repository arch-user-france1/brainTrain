class iostream():
    def addWords(self):
        words = {}
        print("Press ctrl + c if you've finished")
        try:
            while True:
                print("1:   ", end="")
                def1 = input()
                print("2:   ", end="")
                def2 = input()
                words[def1] = def2
        except KeyboardInterrupt:
            return words

    def saveDictionary(self, dictionary, fileName):
        import json
        with open(f"{fileName}.json", "w") as f:
            json.dump(dictionary, f)

    def openDictionary(self, fileName, create=False):
        import json
        try:
            with open(f"{fileName}.json") as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            if create:
                data = {}
                self.saveDictionary(dictionary=data, fileName=fileName)
                return data
            else:
                return None

    def shuffleDictionary(self, dictionary):
        import random
        tuple_list = list(dictionary.items())
        random.shuffle(tuple_list)
        return dict(tuple_list)

    def askFor(self, possibleAnswers, firstAsk=True):
        if firstAsk:
            print("Possible answers are: ", possibleAnswers)
        while True:
            answer = input()
            for i in possibleAnswers:
                if i.lower() == answer.lower():
                    return answer
            print("Possible answers are ", possibleAnswers, ", but you answered ", answer,
                  ". Please answer to one of the possible answers.")

    def tolerateSemicolon(self, string):
        if ';' in string:
            string = string.replace(';', '')
            string = string.split()
        return string

    def tolerateSentence(self, string, string2):
        isSentence = False
        if '.' in string or '!' in string or '?' in string:
            if str(string2[0]).isupper():
                isSentence = True
                stringArr = list(string)
                string = ''
                string += stringArr[0]
                string = string.upper()
                for i in range(len(stringArr) - 1):
                    string += stringArr[i + 1]
        return isSentence, string

    def checkAnswer(self, answer, correctAnswer, removeSpaces):
        correct = True
        correctAnswer = self.tolerateSemicolon(correctAnswer)

        # define your toleration script here
        def tolerateSpaces(i):
            """ toleration of too many or missing spaces """
            if removeSpaces:
                if type(i) == list:
                    for count in range(len(i)):
                        i[count] = i.replace(' ', '')
                elif type(i) == string:
                    i = i.replace(' ', '')

            return i

        def tolerateMultipleSpaces(i):
            """ toleration of more than one space: '  ' => ' ' """
            self.space = False
            self.iArr = list(i)
            i = ''
            for x in self.iArr:
                if x == ' ':
                    if not self.space:
                        i += x
                    else:
                        self.space=True
                else:
                    self.space = False
                    i += x
            return i

        # add your toleration-definition into the following block
        def toleration(defString, isAnswer=False):
            change = False
            defStringOld = defString
            ### ###
            defString = tolerateSpaces(defString)                          # remove all whitespaces
            defString = tolerateMultipleSpaces(defString)                  # remove multiple spaces

            if isAnswer:
                defString = self.tolerateSentence(defString, correctAnswer)[1]                # "hello world!" => "Hello world!"
            ### ###

            # Has the string changed?
            if defString != defStringOld:
                change = True

            return [defString, change]

        #  If the answer has a ; it will be converted into a list.
        if type(correctAnswer) == list:
            isList = True
            answer = self.tolerateSemicolon(answer)  # example: "proud; haughty" => ["proud", "haughty"]
            answer, isChange = toleration(answer, isAnswer=True)
        else:
            isList = False
            answer, isChange = toleration(answer, isAnswer=True)
            correctAnswer = toleration(correctAnswer)[0]

        if isList:
            # modify the answer list
            correctAnswerArr = []
            for i in correctAnswer:
                correctAnswerArr.append(toleration(i)[0])
            for i in answer:
                if i not in correctAnswerArr:
                    correct = False
                    break

        else:
            if answer != correctAnswer:
                correct = False

        return [correct, isChange]
