from collections import defaultdict
import itertools
import random
import urllib.request
import ssl
import numpy as np
from scipy import spatial
from gensim.models.word2vec import Word2Vec
import gensim.downloader as api
from codenames_gym import CodenameEnv as cenv 
from codenames_gym import Card
from sklearn.metrics.pairwise import cosine_similarity

def softmax(x):
    return np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum()

#scores = [3.0, 1.0, 0.2]
#print(softmax(scores))

class CodenamesAgent:

    def __init__():
        pass

    def get_action():
        pass

class RandomSpyAgent(CodenamesAgent):
    
    def __init__(self, team):
        
        self.words = self.make_words_list()
        #corpus = api.load('text8')
        #self.words = list(corpus)
        
        self.team = team

    def make_words_list(self):
        context = ssl._create_unverified_context()
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        req = urllib.request.Request(word_site)
        response = urllib.request.urlopen(req, context=context)
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

class WordEmbeddingsFieldAgent(CodenamesAgent):

    def __init__(self, team, env):
        self.team = team
        self.env = env
        self.model = Word2Vec.load("huihan.model")

    def get_action(self,clue,number):
        #corpus = api.load('text8')
        #print(list(corpus))
        #model = Word2Vec(corpus)
        #w2v_model = gensim.models.Word2Vec(text_data, size=100, min_count=1, window=5, iter=50)
        #model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
        clue_vec = self.model.wv[clue]
        lst = [spatial.distance.cosine(self.model.wv[x.word], clue_vec) for x in self.env.words]
        lst = np.array(lst) * -1
        most_similar_indices = lst.argsort()[-number:][::-1]
        # print(most_similar_indices)
        return np.array(self.env.words)[most_similar_indices]
        
        #words = model.similar_by_vector(word_vec, topn=env.max_guesses, restrict_vocab=None)
        #words = model.wv.most_similar(positive=[word_vec], topn=env.max_guesses)
        #for x in words:
        #    yield Card(x, team="blue", chosen=False)


class SamyakSpyAgent(CodenamesAgent):
    
    def __init__(self, team, env, t):
        
        model = Word2Vec.load("huihan.model")
        self.words = self.make_words_list()
        self.team = team
        self.env = env
        self.R = defaultdict(list)
        self.red_words = [env.words[idx].word for idx in env.rbs[team]]
        for red_word in self.red_words:
            for word in self.words:
                try:
                    self.R[red_word].extend([spatial.distance.cosine(model.wv[word], model.wv[red_word])])
                except Exception as e:
                    self.R[red_word].extend([float("inf")])
        self.B = defaultdict(list)
        self.bad_indices = [idx for idx in range(len(env.words)) if idx not in env.rbs[self.team]]
        self.bad_words = [env.words[idx] for idx in self.bad_indices ]
        for bad_word in self.bad_words:
            for word in self.words:
                try:
                    self.B[bad_word].extend([spatial.distance.cosine(model.wv[word], model.wv[bad_word])])
                except:
                    self.B[bad_word].extend([float("inf")])
        self.t = t

    def make_words_list(self):
        # context = ssl._create_unverified_context()
        # word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        # req = urllib.request.Request(word_site)
        # response = urllib.request.urlopen(req, context=context)
        # txt = response.read()
        # WORDS = txt.splitlines()
        # return WORDS
        words = open("google-10000-english-no-swears.txt")
        words = words.readlines()
        words = [word[:-1] for word in words]
        return words

    def update_redwords(self):
        self.red_words = [self.env.words[idx].word for idx in self.env.rbs[self.team] if not self.env.words[idx].chosen]

    def get_action(self):
        C_i = 0
        best = None
        d = float("inf")
        for i in range(1, len(self.red_words) + 1):
            for rc in itertools.combinations(self.red_words, i):
                for word in range(len(self.words)):
                    if self.words[word] in [card.word for card in self.env.words]:
                        continue
                    else:
                        wd = float("inf")
                        for bad_word in self.bad_words:
                            if self.B[bad_word][word] < wd:
                                wd = self.B[bad_word][word]
                            dr = 0
                            for red_word in rc:
                                if self.R[red_word][word] > dr:
                                    dr = self.R[red_word][word]
                                if dr < d and dr < wd and dr < self.t:
                                    d = dr
                                    best = self.words[word]
                                    C_i = i
        return [best, C_i] 

    


