import random
import urllib.request
import ssl
import numpy as np
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

    def __init__(self, team):
        self.team = team

    def get_action(self, env):
        #corpus = api.load('text8')
        #print(list(corpus))
        #model = Word2Vec(corpus)
        #w2v_model = gensim.models.Word2Vec(text_data, size=100, min_count=1, window=5, iter=50)
        #model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
        model = Word2Vec.load("huihan.model")
        word_vec = model.wv[env.hint]

        lst = [cosine_similarity(x.word, env.hint) for x in env.words]
        print(lst)

        #words = model.similar_by_vector(word_vec, topn=env.max_guesses, restrict_vocab=None)
        words = model.wv.most_similar(positive=[word_vec], topn=env.max_guesses)
        for x in words:
            yield Card(x, team="blue", chosen=False)


class SamyakSpyAgent(CodenamesAgent):
    
    def __init__(self, team):
        
        #self.words = self.make_words_list()
        model = Word2Vec.load("huihan.model")
        self.words = list(model.wv.vocab.keys())
        
        self.team = team

    def make_words_list(self):
        # context = ssl._create_unverified_context()
        # word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        # req = urllib.request.Request(word_site)
        # response = urllib.request.urlopen(req, context=context)
        # txt = response.read()
        # WORDS = txt.splitlines()
        # return WORDS
        return 'Samyak'

    def get_action(self, env):
        #print("before bag")
        #ja mapelle voiture





        return (random.choice(self.words), random.randint(1, 16))

    


