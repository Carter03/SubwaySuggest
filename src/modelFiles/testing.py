import tensorflow as tf
import keras
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Flatten
import numpy as np
from keras.losses import CategoricalCrossentropy
from keras.metrics import CategoricalAccuracy
import datamanager

dataManager = datamanager.DataManager()

maps, x_train, y_train = dataManager.GetData()
y_cat_train = keras.utils.np_utils.to_categorical(y_train)

# print(list(zip(x_train, y_train)))

#aight so we do this trust

def model_thing():
    model = Sequential()
    model.add(Flatten(input_shape=(2,)))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(y_train.max() + 1, activation='softmax'))
    return model

loss_func = CategoricalCrossentropy(reduction='none')
optimzer = Adam(learning_rate=(0.001))

model = model_thing()

top_3_acc = CategoricalAccuracy()

@tf.function
def show_top_3_pred(inputs, targets):
    with tf.GradientTape() as tape:
        predictions = model(inputs, training=True)
        loss = loss_func([targets], predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimzer.apply_gradients(zip(gradients, model.trainable_variables)) # update the gradients manuallyyyy

    top_3_acc.update_state(targets, predictions)

    return loss

EPOCHS = 20

for i in range(EPOCHS):
    for batch_in, batch_tar in zip(x_train, y_cat_train):
        loss = show_top_3_pred(batch_in.reshape(1, 2), batch_tar)

    print(f"Epoch {i + 1}, Loss: {loss}, Top-3 Accuracy: {top_3_acc.result()}")
    top_3_acc.reset_states()