"""
Script to train a classification model on images, save the model, and plot the training results

Adapted from: https://www.tensorflow.org/tutorials/images/classification
"""

import pathlib
from typing import List, Tuple

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers.experimental.preprocessing import Rescaling

# setup global constants
DATA_DIR = "./castings_data"
WEIGHTS_DIR = "./weights"
RESULTS = "training_results.png"
EPOCHS = 10
BATCH_SIZE = 32
IMG_HEIGHT = 180
IMG_WIDTH = 180


def prepare_data() -> Tuple[tf.data.Dataset, tf.data.Dataset, List[str]]:
   """
   Generate training and validation datasets from a folder of images.

   Returns:
      train_ds (tf.data.Dataset): Training dataset.
      val_ds (tf.data.Dataset): Validation dataset.
      class_names (List[str]): Names of all classes to be classified.
   """

   train_dir = pathlib.Path(DATA_DIR, "train")
   validation_dir = pathlib.Path(DATA_DIR, "validation")

   train_ds = tf.keras.preprocessing.image_dataset_from_directory(
      train_dir,
      image_size=(IMG_HEIGHT, IMG_WIDTH),
      batch_size=BATCH_SIZE,
   )

   val_ds = tf.keras.preprocessing.image_dataset_from_directory(
      validation_dir,
      image_size=(IMG_HEIGHT, IMG_WIDTH),
      batch_size=BATCH_SIZE,
   )

   class_names = train_ds.class_names

   return train_ds, val_ds, class_names


def train_and_save_model(
   train_ds: tf.data.Dataset, val_ds: tf.data.Dataset, class_names: List[str]
) -> tf.keras.callbacks.History:
   """
   Train and save a classification model on the provided data.

   Args:
      train_ds (tf.data.Dataset): Training dataset.
      val_ds (tf.data.Dataset): Validation dataset.
      class_names (List[str]): Names of all classes to be classified.

   Returns:
      history (tf.keras.callbacks.History): A History object containing recorded events from
               model training.
   """

   num_classes = len(class_names)

   model = Sequential(
      [
            Rescaling(1.0 / 255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
            layers.Conv2D(16, 3, padding="same", activation="relu"),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding="same", activation="relu"),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding="same", activation="relu"),
            layers.MaxPooling2D(),
            layers.Dropout(0.2),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dense(num_classes),
      ]
   )

   model.compile(
      optimizer="adam",
      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
      metrics=["accuracy"],
   )

   print(model.summary())
   history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)
   model.save(WEIGHTS_DIR)

   return history


def plot_training_results(history: tf.keras.callbacks.History) -> None:
   """
   Plot training and validation accuracy and loss curves, and save the plot.

   Args:
      history (tf.keras.callbacks.History): A History object containing recorded events from
               model training.
   """
   acc = history.history["accuracy"]
   val_acc = history.history["val_accuracy"]
   loss = history.history["loss"]
   val_loss = history.history["val_loss"]
   epochs_range = range(EPOCHS)

   plt.figure(figsize=(16, 8))
   plt.subplot(1, 2, 1)
   plt.plot(epochs_range, acc, label="Training Accuracy")
   plt.plot(epochs_range, val_acc, label="Validation Accuracy")
   plt.legend(loc="lower right")
   plt.title("Training and Validation Accuracy")

   plt.subplot(1, 2, 2)
   plt.plot(epochs_range, loss, label="Training Loss")
   plt.plot(epochs_range, val_loss, label="Validation Loss")
   plt.legend(loc="upper right")
   plt.title("Training and Validation Loss")
   plt.savefig(RESULTS)


if __name__ == "__main__":
   train_ds, val_ds, class_names = prepare_data()
   history = train_and_save_model(train_ds, val_ds, class_names)
   plot_training_results(history)