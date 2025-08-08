# rl_recommender.py
import gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.envs import DummyVecEnv

class InvestmentEnv(gym.Env):
    def __init__(self, token_data, budget=1000):
        super(InvestmentEnv, self).__init__()
        self.token_data = token_data
        self.budget = budget
        self.current_step = 0
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(token_data),), dtype=np.float32)
        self.action_space = gym.spaces.Box(low=0, high=1, shape=(len(token_data),), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        self.budget = 1000
        return np.random.rand(len(self.token_data))

    def step(self, action):
        investment = action * self.budget
        reward = np.dot(investment, np.random.rand(len(self.token_data)))  # Simulated ROI
        self.current_step += 1
        done = self.current_step > 20
        return np.random.rand(len(self.token_data)), reward, done, {}

class RLRecommender:
    def __init__(self, token_data):
        self.env = DummyVecEnv([lambda: InvestmentEnv(token_data)])
        self.model = PPO("MlpPolicy", self.env, verbose=0)

    def train(self, timesteps=10000):
        self.model.learn(total_timesteps=timesteps)
        self.model.save("rl_agent.zip")

    def recommend(self, state):
        self.model = PPO.load("rl_agent.zip")
        action, _ = self.model.predict(state)
        return action

# Example:
# agent = RLRecommender(token_data=[...])
# agent.train()
# print(agent.recommend(np.random.rand(10)))