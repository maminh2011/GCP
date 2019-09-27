import unittest

import model
import numpy as np
import tensorflow as tf

SPACE_SHAPE = (4,)
ACTION_SIZE = 2
LEARNING_RATE = .2
HIDDEN_NEURONS = 20

MEMORY_SIZE = 3
MEMORY_BATCH_SIZE = 3
GAMMA = .5

EXPLORE_DECAY = .9

FAKE_STATES = np.array([[-.1, .2], [-.9, -.3], [.4, .5]], dtype=np.float32)
FAKE_ACTIONS = np.array([0, 1, 1])
FAKE_NEW_STATES = np.array([[-.9, -.3], [.4, .5], [0, 0]], dtype=np.float32)
FAKE_REWARD = np.array([0, 0, 100], dtype=np.float32)
FAKE_DONE = np.array([False, False, True])


class TestAgentMethods(unittest.TestCase):

    def setUp(self):
        network = model.deep_q_network(
            SPACE_SHAPE, ACTION_SIZE, LEARNING_RATE, HIDDEN_NEURONS)
        memory = model.Memory(MEMORY_SIZE, MEMORY_BATCH_SIZE, GAMMA)
        self.agent = model.Agent(network, memory, EXPLORE_DECAY, ACTION_SIZE)

    def test_get_target_qs(self):
        self.agent.memory.buffer = ["fake_memory", "fake_memory", "fake_memory"]
        self.agent.memory.sample = unittest.mock.MagicMock(return_value=(
            FAKE_STATES, FAKE_ACTIONS, FAKE_NEW_STATES, FAKE_REWARD, FAKE_DONE)
        )
        self.agent.network.fit = unittest.mock.MagicMock()

        fake_qs_current_state = tf.constant([[1., 2.], [4., 3.], [5., 6.]])
        fake_qs_state_prime = tf.constant([[4., 3.], [5., 6.], [8., 7.]])
        self.agent.network.predict = unittest.mock.MagicMock(
            side_effect=[fake_qs_state_prime, fake_qs_current_state])
        expected_target_qs = tf.constant([[2., 2.], [4., 3.], [5., 100.]])
        self.agent.learn()
        
        self.agent.network.fit.assert_called_with(
            FAKE_STATES, expected_target_qs,
            batch_size=MEMORY_BATCH_SIZE, epochs=1, verbose=0
        )


if __name__ == '__main__':
    unittest.main()