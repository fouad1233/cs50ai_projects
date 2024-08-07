# Models i try

First i begin with trying this model, it's a little big. The model is as following:

```
my_model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])
    my_model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
```

When i try this model i see that is have good accuracy the test output with small dataset is as following: 

`11/11 - 0s - 11ms/step - accuracy: 0.9970 - loss: 0.0055`

I try to use a more small model by removing the second convulotion and polling layers as following:

```
my_model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])
    my_model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
```

it results also with a good accuracy as following:

`11/11 - 0s - 10ms/step - accuracy: 0.9881 - loss: 0.1032`

When trying decrase the number of the convolution filter as following from 16 to 2 as following:

```
my_model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(2, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])
    my_model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
```

the accuracy change as follow :

`11/11 - 0s - 10ms/step - accuracy: 0.9792 - loss: 0.5541`

and by removing the convulation and polling it wil be :

`11/11 - 0s - 8ms/step - accuracy: 0.9762 - loss: 1.4330`

the loss rate increase so much
