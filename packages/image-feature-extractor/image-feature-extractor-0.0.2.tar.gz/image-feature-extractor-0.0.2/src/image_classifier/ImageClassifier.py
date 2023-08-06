from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageClassifier(object):

    def __init__(self, model=None):
        # initializing the model
        # if no saved model is provided, then download resnet50 and tune it
        self.img_size = 224
        if model is None:
            self.init_model = ResNet50(weights='imagenet', include_top=False,
                                       input_shape=(self.img_size, self.img_size, 3),
                                       pooling='max')
        self.model = model

    def _model(self, tune_from, num_classes, lr):
        self.init_model.trainable = True
        # Fine-tune from this layer onwards
        fine_tune_at = tune_from
        # Freeze all the layers before the `fine_tune_at` layer
        for layer in self.init_model.layers[:fine_tune_at]:
            layer.trainable = False
        resnet50_x = Flatten()(self.init_model.output)
        resnet50_x = Dense(num_classes, activation='softmax')(resnet50_x)
        resnet50_x_final_model = Model(inputs=self.init_model.input, outputs=resnet50_x)
        base_learning_rate = lr
        resnet50_x_final_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
                                       loss=tf.keras.losses.categorical_crossentropy,
                                       metrics=['accuracy'])

        self.model = resnet50_x_final_model

    def fit(self, train_data, val_data, epochs, tune_from=120, num_classes=5, lr=0.0001):
        if not self.model:
            self._model(tune_from, num_classes, lr)
        history_fine = self.model.fit(train_data,
                                      epochs=epochs, validation_data=val_data, batch_size=32)
        return self.model, history_fine

    def predict(self, image_path):
        if self.model is not None:
            img = image.load_img(image_path, target_size=(self.img_size, self.img_size))
            img_tensor = image.img_to_array(img)  # (height, width, channels)
            img_tensor = np.expand_dims(img_tensor,
                                        axis=0)
            img_tensor /= 255.  # imshow expects values in the range [0, 1]
            classes_prob = self.model.predict(img_tensor)
            return classes_prob
