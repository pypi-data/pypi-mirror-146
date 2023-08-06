import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import numpy as np


class ExtractFeatureVectors(object):

    def __init__(self, model=None):
        # initializing the model
        self.init_model = model
        self.model = None
        self._model()

    def _model(self):
        img_size = 224
        if self.init_model:
            from tensorflow.keras.models import Model

            self.model = Model(inputs=self.init_model.input,
                               outputs=self.init_model.layers[-2].output)
        else:
            base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3), pooling='max')
            # Customize the model to return features from fully-connected layer
            self.model = base_model

    def extract(self, input_image):
        if self.model is not None:
            # Resize the image
            img = input_image.resize((224, 224))
            # Convert the image color space
            img = img.convert('RGB')
            # Reformat the image
            x = image.img_to_array(img)
            # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
            img_tensor = np.expand_dims(x, axis=0)
            # if self.init_model:
            #    img_tensor /= 255.
            # else:
            input_to_model = preprocess_input(img_tensor)
            # Extract Features
            feature = self.model.predict(input_to_model)[0]
            return feature / np.linalg.norm(feature)

