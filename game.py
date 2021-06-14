from codenames_gym import CodenameEnv
from agent import SamyakSpyAgent, WordEmbeddingsFieldAgent
import IPython
e = IPython.embed

def game():
    env = CodenameEnv()
    spy = SamyakSpyAgent('blue', env, 5)
    # spy = RandomSpyAgent('blue')
    # operative = RandomFieldAgent('blue')
    operative = WordEmbeddingsFieldAgent('blue', env)
    round_num = 0
    while spy.red_words:
        print(f"\n================================\nRound{round_num} board:")
        env.render()
        print("================================")

        spy_move = spy.get_action()
        print(f"Spy agent's hint        : {spy_move}")
        _ = env.step(spy_move, spy.team, spyagent=True)

        field_reward = 0
        for i, action in enumerate(list(operative.get_action(env.hint,env.max_guesses))):
            print(f"Field agent's guess #{i+1}/{env.max_guesses}: \"{action}\"")
            obs, reward, done, info = env.step((action, i), operative.team)

            spy.update_redwords()
            field_reward += reward
            print(f"Environment             : {info['type']}")
            print(f"Total reward            : {field_reward}\n")

            if done:
                break
        round_num += 1

if __name__ == "__main__":
    game()
