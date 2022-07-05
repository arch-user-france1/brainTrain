import io


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

    def checkAnswer(self, answer, correctAnswer):
        correct = True
        correctAnswer = self.tolerateSemicolon(correctAnswer)
        if type(correctAnswer) == list:
            isArray=True
        else:
            isArray=False
        if isArray:
            answer = self.tolerateSemicolon(answer)
            print(answer)

            for i in answer:
                print(i)
                if i not in correctAnswer:
                    print(f"{i} is not in {correctAnswer}")
                    correct = False
                    break
        else:
            if answer != correctAnswer:
                correct = False

        return correct