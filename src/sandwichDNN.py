import keras
import datamanager

class SandwichModel:
    def __init__(self):
        dm = datamanager.DataManager()
        self.maps, self.x_train, self.y_train = dm.GetData()
        self.y_cat_train = keras.utils.to_categorical(self.y_train)
        self.model = keras.models.Sequential()

    def Fit(self):
        self.model.add(keras.layers.Flatten(input_shape = (2,)))

        self.model.add(keras.layers.Dense(64, activation='relu'))
        self.model.add(keras.layers.Dense(64, activation='relu'))

        self.model.add(keras.layers.Dense(self.y_train.max() + 1, activation='softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model.fit([self.x_train], self.y_cat_train, epochs=25, verbose=0)

    def Predict(self, input : list, predNum : int):
        ids = self.model.predict([input], verbose=0).argsort()[0][-predNum:][::-1] # top predNum predictions
        return [list(self.maps[0].keys())[list(self.maps[0].values()).index(i)] for i in ids]

if __name__ == '__main__':
    model = SandwichModel()
    model.Fit()

    for i in range(5):
        ids = model.Predict([i, 0], 3)
        print(f'{i} age, male')
        # print(list(model.maps[0]))
        print([list(model.maps[0].keys())[list(model.maps[0].keys()).index(i)] for i in ids])
    for i in range(5):
        ids = model.Predict([i, 1], 3)
        print(f'{i} age, female')
        # print(list(model.maps[0]))
        print([list(model.maps[0].keys())[list(model.maps[0].keys()).index(i)] for i in ids])