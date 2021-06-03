from codenames_gym import CodenameEnv
from agent import *


def game():
    environment = CodenameEnv()
    #spy = RandomSpyAgent('blue')
    spy = SamyakSpyAgent('blue', environment, 5)
    #operative = RandomFieldAgent('blue')
    operative = WordEmbeddingsFieldAgent('blue', environment)
    while spy.red_words:
        print("BOARD")
        environment.render()
        print("================================")
        # 1 iteration
        spy_move = spy.get_action()
        a,b,c,d = environment.step(spy_move, spy.team, spyagent=True)
        print("SPY MOVE")
        print(spy_move)
        print()
        environment.render()
        
        print("================================")
        print()
        print(environment.max_guesses)
        field_reward = 0
        for i, action in enumerate(list(operative.get_action(environment.hint,environment.max_guesses))):
            print(action)
            e,f,g,h= environment.step((action, i), operative.team)
            spy.update_redwords()
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
