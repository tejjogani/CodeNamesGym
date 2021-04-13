from codenames_gym import CodenameEnv
from agent import *


def game():
    environment = CodenameEnv()
    #spy = RandomSpyAgent('blue')
    spy = SamyakSpyAgent('blue')
    #operative = RandomFieldAgent('blue')
    operative = WordEmbeddingsFieldAgent('blue')
    print("INITIAL BOARD")
    environment.render()
    print("================================")
    # 1 iteration
    spy_move = spy.get_action(environment)
    print("before spy")
    print(spy_move)
    print("after spy")
    a,b,c,d = environment.step(spy_move, spy.team, spyagent=True)
    print("SPY MOVE")
    print()
    environment.render()
    
    print("================================")
    print()
    print(environment.max_guesses)
    field_reward = 0
    '''
    for i in range(environment.max_guesses):
        guess = operative.get_action(environment)
        print(guess)
        e,f,g,h= environment.step((guess, i), operative.team)
        field_reward += f
        print("FIELD MOVE")
        print()
        environment.render()
        
        print("================================")
        print()

        if g:
            print("DONE")
            print("AGENT REWARD: ", field_reward)
            break
    '''
    for i, action in enumerate(list(operative.get_action(environment))):
        print(action)
        e,f,g,h= environment.step((action, i), operative.team)
        field_reward += f
        print("FIELD MOVE")
        print()
        environment.render()
        
        print("================================")
        print()
        if g:
            print("DONE")
            print("AGENT REWARD: ", field_reward)
            break

if __name__ == "__main__":
    game()
