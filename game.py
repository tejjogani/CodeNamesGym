from codenames_gym import CodenameEnv
from agent import RandomSpyAgent, RandomFieldAgent


def game():
    environment = CodenameEnv()
    spy = RandomSpyAgent('blue')
    operative = RandomFieldAgent('blue')
    print("INITIAL BOARD")
    environment.render()
    print("================================")
    # 1 iteration
    spy_move = spy.get_action(environment)
    print(spy_move)
    a,b,c,d = environment.step(spy_move, spy.team, spyagent=True)
    print("SPY MOVE")
    print()
    environment.render()
    
    print("================================")
    print()
    print(environment.max_guesses)
    for i in range(environment.max_guesses):
        guess = operative.get_action(environment)
        print(guess)
        e,f,g,h= environment.step((guess, i), operative.team)
        print("FIELD MOVE")
        print()
        environment.render()
        
        print("================================")
        print()

        if g:
            print("DONE")
            break

if __name__ == "__main__":
    game()
