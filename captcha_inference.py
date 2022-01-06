from keras.models import load_model
import tensorflow as tf
import numpy as np
import keras
import cv2

class CaptchaSolver:
    def __init__(self, model_path, char_path):
        self.model = load_model(model_path)
        self.MAX_LENGTH = 6 # Num of characteres on a captcha

        # Mapping integers back to original characters
        self.num_to_char_model = load_model(char_path)

    # A utility function to decode the output of the network
    def decode_batch_predictions(self, pred):
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        # Use greedy search. For complex tasks, you can use beam search
        results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][:,:self.MAX_LENGTH]
        # Iterate over the results and get back the text
        output_text = []
        for res in results:
            res = tf.strings.reduce_join(self.num_to_char_model(res)).numpy().decode("utf-8")
            output_text.append(res)
        return output_text

    def morphologyFilter(self, image, threshold=0.5):
        image = (image.astype(np.float32) / 255.0)
        image = np.where(image >= threshold, 0.0, 1.0)
        image = (image * 255).astype(np.uint8)

        kernel =  np.ones((3, 3), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.dilate(image, kernel, iterations=1)

        image = np.where(image == 0, 255, 0).astype(np.uint8)

        return image

    def solveCaptcha(self, image):
        image = cv2.resize(image, (180, 50))
        image = self.morphologyFilter(image)
        image = image.astype(np.float32) / 255.0
        image = np.expand_dims(image, axis=-1)
        image = np.transpose(image, axes=(1, 0, 2))
        preds = self.model.predict(np.expand_dims(image, axis=0))
        captcha = self.decode_batch_predictions(preds)

        return captcha

if __name__ == '__main__':
    captchaSolver = CaptchaSolver('models/prediction_captcha_model.h5', 'models/num_to_char_model.h5')

    image = cv2.imread('data/captcha_dataset/1EbzUd.png', cv2.IMREAD_GRAYSCALE)
    print(captchaSolver.solveCaptcha(image))