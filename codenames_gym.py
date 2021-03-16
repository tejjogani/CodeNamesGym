import gym
from gym import spaces
import numpy as np

def random_team():
  return 'red' if np.random.randint(1) == 1 else 'blue'


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
    self.team = random_team()
    self.words = list(map(lambda x: dictionary[x] ,list(np.random.randint(low=1, high=100, size=25))))
    self.rbs = {'red': [], 'blue': []}
    self.rbs['red'], self.rbs['blue'] = self.fill_team('red'), self.fill_team('blue')

    

  def step(self, action):
    # Execute one time step within the environment
    assert len(action.split('')) == 1 



    pass
  def reset(self):
    # Reset the state of the environment to an initial state
    pass
  def render(self, close=False):
    # Render the environment to the screen
    pass

  def other(color):
    assert color in ['red', 'blue']
    return 'red' if color == 'blue' else 'blue'

  def fill_team(color):
    if self.rbs[self.other(color)]:
      for i in range(8):
        x = np.random.randint(25)
        while x in self.rbs[color] and not x in self.rbs[self.other(color)]:
          x = np.random.randint(25)
      self.rbs[color].append(x)
    else:
      for i in range(8):
        x = np.random.randint(25)
        while x in self.rbs[color]:
          x = np.random.randint(25)
        self.rbs[color].append(x)
