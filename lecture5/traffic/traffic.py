import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import time
from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    
    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    print("Fitting model on training data")
    fit_start_time = time.time()
    model.fit(x_train, y_train, epochs=EPOCHS)
    fit_end_time = time.time()
    print(f"Model fit in {fit_end_time - fit_start_time} seconds.")
    

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    print(sys.argv)
    print(len(sys.argv))
    print(sys.argv[2])
    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    for sub_dir in os.listdir(data_dir):
        #if its a directory beetwen 0 and NUM_CATEGORIES
        if not sub_dir.isdigit() or int(sub_dir) >= NUM_CATEGORIES:
            continue
        else:
            print("Loading images from: ", os.path.join(data_dir, sub_dir))
            new_dir = os.path.join(data_dir, sub_dir)
            for image in os.listdir( new_dir ):
                print("Loading image: ", image)
                
                read_time = 0
                read_time_start = time.time()
                img = cv2.imread(os.path.join(new_dir, image))
                read_time_end = time.time()
                print(f"Image read in {read_time_end - read_time_start} seconds.")
                resize_time = 0
                resize_time_start = time.time()
                new_image = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                resize_time_end = time.time()
                print(f"Image resized in {resize_time_end - resize_time_start} seconds.")
                images.append(new_image)
                labels.append(int(sub_dir))
                print(len(images), len(labels))
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
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
    return my_model


if __name__ == "__main__":
    main()
