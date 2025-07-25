"""
Traffic Sign Classification using Neural Networks

Neural network to classify traffic signs using TensorFlow and computer vision
"""

import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
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
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

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
    of the images in the data directory, where each image is a numpy ndarray
    with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should be a list of
    integer labels, corresponding to the categories in `images`.
    """
    images = []
    labels = []
    
    # Iterate through each category directory
    for category in range(NUM_CATEGORIES):
        category_path = os.path.join(data_dir, str(category))
        
        if os.path.exists(category_path):
            # Iterate through all images in the category directory
            for filename in os.listdir(category_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.ppm')):
                    # Load and process image
                    image_path = os.path.join(category_path, filename)
                    image = cv2.imread(image_path)
                    
                    if image is not None:
                        # Resize image to standard dimensions
                        image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
                        
                        # Convert from BGR to RGB
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                        # Add image and label to lists
                        images.append(image)
                        labels.append(category)
    
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([
        # Convolutional layer with 32 filters, 3x3 kernel, ReLU activation
        tf.keras.layers.Conv2D(
            32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        
        # Max pooling layer with 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        
        # Second convolutional layer with 64 filters
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        
        # Second max pooling layer
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        
        # Third convolutional layer with 64 filters
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        
        # Flatten layer to convert 2D feature maps to 1D
        tf.keras.layers.Flatten(),
        
        # Dense hidden layer with 128 units and ReLU activation
        tf.keras.layers.Dense(128, activation='relu'),
        
        # Dropout layer to prevent overfitting
        tf.keras.layers.Dropout(0.5),
        
        # Output layer with NUM_CATEGORIES units and softmax activation
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


if __name__ == "__main__":
    main()