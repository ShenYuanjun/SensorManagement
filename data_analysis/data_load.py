import pickle

mark = 'env_test_0704'

with open(mark + '.pkl', 'rb') as f:
    b = pickle.load(f)