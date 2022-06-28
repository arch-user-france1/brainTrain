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
            else:
                return None
        return data

    def shuffleDictionary(self, dictionary):
        import random
        tuple_list = list(dictionary.items())
        random.shuffle(tuple_list)
        return dict(tuple_list)

    def askFor(self, possibleAnswers):
        print("Possible answers are: ", possibleAnswers)
        while True:
            answer = input()
            for i in possibleAnswers:
                if i.lower() == answer.lower():
                    return answer
            print("Possible answers are ", possibleAnswers, ", but you answered ", answer,
                  ". Please answer to one of the possible answers.")
