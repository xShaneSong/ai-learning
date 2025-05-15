import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation

model = Sequential([
    Dense(4, keras.Input(shape=(2,))),
    Activation('sigmoid'),
    Dense(1),
    Activation('sigmoid'),
])

training_number = 100
training_data = np.random.rand((training_number, 2))
labels = [(1 if data[0] > data[1] else 0) for data in training_data]
model.fit(training_data, labels, epochs = 20, batch_size = 32)

test_number = 100
test_data = np.random.rand((test_number, 2))
expected = [(1 if data[0] > data[1] else 0) for data in test_data]
error = 0
for i in range(test_number):
    prediction = model.predict(test_data[i])
    if prediction != expected[i]:
        error += 1
print('error rate: {}'.format(error / test_number))

