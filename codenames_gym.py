import gym
from gym import spaces
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
    self.dictionary = bagOfWords + weebWords
  
    self.team = random_team()
    self.words = list(map(lambda x: Card(self.dictionary[x]) ,gen_random_nums(16))) #temporary
    self.rbs = {'red': [], 'blue': []}
    self.fill_team('red') 
    self.fill_team('blue')
    self.rbs['red'].sort()
    self.rbs['blue'].sort()
    self.correct_words = []
    self.max_guesses = 0
    self.guessed_correct = False

  
  def step(self, action, spyagent=0):
    # Execute one time step within the environment
    done = False
    if not spyagent: #0 is listener
      assert len(action) == 2 and len(action[0].split('')) == 1
      if action in self.correct_words:
        reward = 1 #recognize that sometimes reward is given for random choices (50/50)
        if action[1] == self.max_guesses:
          done = True
          self.guessed_correct =  True
      else:
        reward = -1
        done = True
        self.guessed_correct = False
      self.words[action].chosen = True
    else:
      assert len(action) == 3
      #(keyword, number of words, [indices of words described])
      self.correct_words = action[2]
      self.max_guesses = action[1]
      reward = 1 if self.guessed_correct else -1
      
    
    return self._get_obs(), reward, done, {}

  def reset(self):
    # Reset the state of the environment to an initial state
    for x in self.words:
      x.chosen = False

  """
  TODO: decide with MARL team
  """
  def _get_obs(self):
    return 'awkward pause'
    
  def print_board():
    for i in range(4):
      for j in range(4):
        print(str(self.words[i*4 + j]) +   " " * (20 - len(str((self.words[i*4 + j]))))  , end=" | ")
      print("")

  def render(self, close=False, play=False):
    # Render the environment to the screen
    print_board()
    if play

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
