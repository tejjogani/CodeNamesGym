import gym
import random
from gym import spaces
from gensim.models.word2vec import Word2Vec

import gensim.downloader as api
import numpy as np

def random_team():
  return 'red' if np.random.randint(1) == 1 else 'blue'

def gen_random_nums(size):
  nums = set()
  while len(nums) < size:
    x = np.random.randint(1, 59)
    nums.add(x)
  return nums

bagOfWords = ["Lyft", "Uber", "Tesla", "Facemask", "Coco", "Blueface", "Backpack", "Water", "Car", 
"Poster", "Art", "Plastic", "Phone", "Chair", "Street", "Lamp", "Laptop", "Instagram", "Twitter", 
"Charger", "Acne", "Lightbulb", "Gym", "Dumbbell", "Bench", "Smog", "Book", "Bike", "Scooter",
"Hat", "Beanie", "Sunglasses", "Dart", "Cigarette", "Leather", "Snowboard", "Ice", "Drip", "Vehicle",
"BMW", "Mercedes", "Electricity"] #len = 42
weebWords = ["Naruto", "Sasuke", "Senpai", "Eren", "Jaegar", "Mikasa", "Jujutsu", "Katakana", 
"Nani", "Shinde", "Kirito", "Cheetos", "Asuna", "Shingeki", "Kanji", "Hiragana", "Altoids", "OPM"] #len = 18

class Card:
  def __init__(self, word, team=None, chosen=False):
    self.word = word
    self.team = team
    self.chosen = False
  
  def get_word(self, word):
    return self.word

  def get_team(self, team):
    return self.team
    
  def selected(self, team):
    self.chosen = True
  
  def __str__(self):
    if self.chosen:
      return str(self.team)
    else:
      return str(self.word)

  def __repr__(self):
    if self.chosen:
      return str(self.team)
    else:
      return str(self.word)


"""
to run: python3 -i codenames_gym.py, instantiate CodenameEnv()
"""
class CodenameEnv(gym.Env):
  """Custom Environment that follows gym interface"""

  def __init__(self):
    super(CodenameEnv, self).__init__()
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    '''
    self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
    # Example for using image as input:
    self.observation_space = spaces.Box(low=0, high=255, shape=
                    (HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)
    '''
    #self.dictionary = bagOfWords + weebWords
    model = Word2Vec.load("huihan.model")
    self.dictionary = list(model.wv.index_to_key)
    cn = open("game_wordpool.txt").readlines()
    cn = [word.rstrip().lower() for word in cn]
    self.words = random.sample(cn, 16)
    self.words = [Card(word) for word in self.words]
    self.team = random_team()
    #self.words = list(map(lambda x: Card(self.dictionary[x]) ,gen_random_nums(16))) #temporary
    
    self.rbs = {'red': [], 'blue': []}
    self.fill_team('red') 
    self.fill_team('blue')
    self.death = [random.choice(self.rbs['red']), random.choice(self.rbs['blue'])]
    self.rbs['red'].remove(self.death[0])
    self.rbs['blue'].remove(self.death[1])
    for i in range(2):
      self.words[self.death[i]].team = "DEATH CARD"
    self.rbs['red'].sort()
    self.rbs['blue'].sort()
    self.correct_words = []
    self.max_guesses = 0
    self.guessed_correct = False
    self.hint = ""

  
  def step(self, action, team, spyagent=False):
    # Execute one time step within the environment
    done = False
    if not spyagent: #0 is listener
      print(action)
      assert len(action) == 2 and len(action[0].word.split(' ')) == 1
      if self.words.index(action[0]) in self.death:
        done = True
        reward = -1 
        self.words[self.words.index(action[0])].chosen = True
        return self._get_obs(), reward, done, {}
      if self.words.index(action[0]) in self.rbs[team]:
        reward = 1 #recognize that sometimes reward is given for random choices (50/50)
        if action[1] == self.max_guesses:
          done = True
          self.guessed_correct =  True
      else:
        reward = -1
        done = True
        self.guessed_correct = False
      self.words[self.words.index(action[0])].chosen = True
    else:
      assert len(action) == 3 or len(action) == 2
      #(keyword, number of words, [indices of words described])
      #self.correct_words = action[2]
      self.hint = action[0]
      self.max_guesses = action[1]
      reward = 1 if self.guessed_correct else -1
      
    
    return self._get_obs(), reward, done, {}

  def reset(self):
    # Reset the state of the environment to an initial state
    for x in self.words:
      x.chosen = False

    #needs to return final observation

  """
  TODO: decide with MARL team
  """
  def _get_obs(self):
    return 'awkward pause'
    
  def print_board(self):
    #print("hei")
    for i in range(4):
      for j in range(4):
        print(str(self.words[i*4 + j]) +   " " * (20 - len(str((self.words[i*4 + j]))))  , end=" | ")
      print("")

  def render(self, close=False, play=False):
    # Render the environment to the screen
    self.print_board()

  def other(self, color):
    assert color in ['red', 'blue']
    return 'red' if color == 'blue' else 'blue'

  def fill_team(self, color):
    if self.rbs[self.other(color)] != []:
      for i in range(16):
        if i not in self.rbs[self.other(color)]:
          self.rbs[color].append(i)
          self.words[i].team = color
    else:
      for _ in range(8):
        x = np.random.randint(16)
        while x in self.rbs[color]:
          x = np.random.randint(16)
        self.rbs[color].append(x)
        self.words[x].team = color


  def get_legal_moves(self, team):
    #The spy agent chooses anything so it's unneeded

    #Field Operative

    return self.words

def example():
  print("Codenames Env can be created by running g = CodenameEnv()")
  g = CodenameEnv()
  print("Creating this sets everything up")
  print("g.words")
  print(g.words)
  print("team assignments")
  print(g.rbs)
  print("g.render()")
  print(g.render())
  print("Set cards to chosen with g.words[i].chosen = True")
  print("g.words[3].chosen = True")
  print("g.words[4].chosen = True")
  print("g.words[8].chosen = True")
  g.words[3].chosen = True
  g.words[4].chosen = True
  g.words[8].chosen = True
  g.render()





if __name__ == "__main__":
  example()
