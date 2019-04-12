from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random


class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque()
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.out_threshold = 0.5
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        # each add is another layer with a specified number of neurons
        model.add(Dense(48, input_dim=self.state_size, activation='relu'))
        model.add(Dense(48, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        act_values = self.model.predict(state)
        return act_values[0][0]  # 0 < act_values[0][0] < 1

    def replay(self, batch_size):
        mini_batch = random.sample(self.memory, batch_size)
        for state, _, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = (reward + self.gamma * self.model.predict(next_state)[0][0])
                # int(self.model.predict(next_state)[0][0] < self.out_threshold))
            target_f = self.model.predict(state)
            target_f[0][0] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
