import keras

class SandwichModel:
    def __init__(self, dataManager):
        self.maps, self.x_train, self.y_train = dataManager.GetData()
        self.y_cat_train = keras.utils.np_utils.to_categorical(self.y_train)
        self.model = keras.models.Sequential()

    def Fit(self):
        self.model.add(keras.layers.Flatten(input_shape = (2,)))

        self.model.add(keras.layers.Dense(128, activation='relu'))
        self.model.add(keras.layers.Dense(128, activation='relu'))

        self.model.add(keras.layers.Dense(self.y_train.max() + 1, activation='softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model.fit([self.x_train], self.y_cat_train, epochs=25, verbose=0)

    def Predict(self, input : list, predNum : int):
        ids = self.model.predict([input]).argsort()[0][-predNum:][::-1] # top predNum predictions
        return [list(self.maps[0].keys())[list(self.maps[0].values()).index(i)] for i in ids]

if __name__ == '__main__':
    import datamanager
    dataManager = datamanager.DataManager()

    model = SandwichModel(dataManager)
    model.Fit()

    print(ids := model.Predict([4, 0], 3))
    print([list(model.maps[0].keys())[list(model.maps[0].values()).index(i)] for i in ids])