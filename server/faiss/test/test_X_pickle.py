import pickle 
with open('./X_10.pickle', 'rb') as encodePickle:
    X = pickle.load(encodePickle)

print(X.shape)