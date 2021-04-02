import random
import urllib.request
from codenames_gym import CodenameEnv as cenv 


class CodenamesAgent:

    def __init__():
        pass

    def get_action():
        pass


class RandomSpyAgent(CodenamesAgent):
    
    def __init__(self, team):
        self.words = self.make_words_list()
        self.team = team

    def make_words_list(self):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        req = urllib.request.Request(word_site)
        response = urllib.request.urlopen(req)
        txt = response.read()
        WORDS = txt.splitlines()
        return WORDS

    def get_action(self, env):

        return (random.choice(self.words), random.randint(1, 16))
    
class RandomFieldAgent(CodenamesAgent):
    
    def __init__(self, team):
        self.team = team

    def get_action(self, env):
        return random.choice(env.get_legal_moves(self.team))



    


