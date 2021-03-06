from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, GRU
from keras.layers.recurrent import SimpleRNN
from keras.layers.embeddings import Embedding
from keras.regularizers import l2
from keras.optimizers import RMSprop
import numpy as np
from tqdm import tqdm
import string

dfile = 'shakespear.txt'

with open(dfile,'r') as f:
    raw = f.read()

lowers = string.ascii_lowercase

k = set(raw.lower()) - set(lowers)
''.join(sorted(k))

extra = "\n !?';,."
allowed = set(lowers + extra)
print(allowed)
from collections import Counter, defaultdict

D = dict([(k,k) if k in allowed else (k, ' ') for k in set(raw.lower())])
keys = ''.join(D.keys())
vals = ''.join([D[k] for k in keys])
DD = str.maketrans(keys,vals)

data = raw.lower().translate(DD)
print(data)

# collect repeated spaces and newlines
while '  ' in data:
    data = data.replace('  ',' ')
while '\n\n' in data:
    data = data.replace('\n\n','\n')
while '\n \n' in data:
    data = data.replace('\n \n','\n')

chars = list(lowers+extra)

# change unroll length
maxlen=20
step = 1
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))
print(char_indices)


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(Embedding(len(chars), 48, input_length=maxlen))
model.add(LSTM(64, return_sequences=True))
model.add(LSTM(64, return_sequences=True))
model.add(LSTM(64))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics = ['accuracy'])

epochs = 10
num_blocks = 10


# truncate the data and reshape
data = data[:-(len(data)%num_blocks)]
data = np.array(list(data)).reshape([num_blocks,-1])

for j in tqdm(range(epochs)):
    for b in tqdm(range(num_blocks)):
        sentences = []
        next_chars = []
        for i in range(0, len(data[b]) - maxlen, step):
                sentences.append(data[b,i: i + maxlen])
                next_chars.append(data[b,i + maxlen])
        # stick with dense encoding
        X = np.zeros([len(sentences),maxlen],dtype=np.uint8)
        # encode all in one-hot
        Y = np.zeros([len(sentences),len(chars)],dtype=np.uint8)
        i = 0
        for t, char in enumerate(sentences[0]):
            X[i, t]= char_indices[char]
            Y[i, char_indices[next_chars[i]]] = 1
        for i, sentence in enumerate(sentences[1:]):
            X[i+1, :-1] = X[i, 1:]
            X[i+1, -1] = char_indices[next_chars[i]]
            Y[i+1, char_indices[next_chars[i+1]]] = 1
        model.fit(X,Y,epochs=1,validation_split=0.1)
    model.save_weights('bardicweights_{0}.h5'.format(j))


#model.fit(X,Y,nb_epoch=10)
model.save_weights('bardicweights.h5')
model.load_weights('bardicweights.h5')


