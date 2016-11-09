#%%
import gym
import logging
import numpy as np
import tensorflow as tf
from arguments import args
from agents.DQN.Agent import Agent

def main():
    logging.root.setLevel(logging.INFO)
    env = gym.make(args.env)
    if args.monitor != "":
        env.monitor.start(args.monitor)
    # logging.warning("action space: %s, %s, %s" % (env.action_space, env.action_space.high, env.action_space.low))

    agent = Agent(env)

    for iterations in range(args.iterations):
        agent.reset()
        state = env.reset()
        state = np.array([state])

        done = False
        total_rewards = 0
        steps = 0

        while not done and steps < env.spec.timestep_limit:
            steps += 1

            action = agent.action(state, show=steps % 200 == 0)
            # if steps % 100 == 0:
            #     logging.warning(action[0])
            new_state, reward, done, info = env.step(action[0])
            if steps == env.spec.timestep_limit:
                done = False
            new_state = np.array([new_state])
            agent.feedback(state, action, reward, done, new_state)
            state = new_state

            total_rewards += reward
            if iterations % 10 == 0 and steps % 1 == 0 and args.mode == "infer":
                env.render()
                logging.warning("step: #%d, action = %.3f, reward = %.3f, iteration = %d" % (steps, action[0], reward, iterations))
            # if episode == 0:
            #     print observation, action, info

        logging.warning("iteration #%d: total rewards = %.3f, steps = %d" % (iterations, total_rewards, steps))

    if args.monitor != "":
        env.monitor.close()

if __name__ == "__main__":
    with tf.Session().as_default():
        main()
