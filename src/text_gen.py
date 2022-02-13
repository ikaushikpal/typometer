import requests
from random import randint, choice
from string import ascii_lowercase
from random_word import RandomWords


class TextGenerator:
    def __init__(self):
        self.isConnected()
        self.randObj = None

    def isConnected(self):
        response = requests.get("https://1.1.1.1/")
        if response.status_code == 200:
            self.internet = True
        else:
            self.internet = False
    
    def generate(self, word_count:int, min_length:int=3, max_length:int=8) -> str:
        self.words = []

        if self.internet:
            if self.randObj == None:
                self.randObj = RandomWords()
            self.__online(word_count, min_length, max_length)
        else:
           self.__offline(word_count, min_length, max_length)

        return ' '.join(self.words)

    def __online(self, word_count:int, min_length:int, max_length:int) -> str:
        if word_count == 0:
            return
        count = 0
        
        for word in self.randObj.get_random_words(hasDictionaryDef="true", minLength=min_length, maxLength=max_length, limit=word_count):
            if word.isalpha():
                self.words.append(word.lower())
                count += 1
        
        self.__online(word_count-count, min_length, max_length)
        
    def __offline(self, word_count:int, min_length:int, max_length:int):
        for _ in range(word_count):
            max_range = randint(min_length, max_length)
            word = ''.join([choice(ascii_lowercase) for _ in range(max_range)])
            self.words.append(word)
        