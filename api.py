from flask import Flask, request
from captcha_inference import CaptchaSolver
import base64
import numpy as np
import cv2

app = Flask(__name__)
captchaSolver = CaptchaSolver('models/prediction_captcha_model.h5', 'models/num_to_char_model.h5')

@app.route("/captcha", methods=['POST'])
def solveCaptcha():
    captcha_request = request.get_json()

    im_b64 = captcha_request['image'].encode('utf-8')

    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    image = cv2.imdecode(im_arr, flags=cv2.IMREAD_GRAYSCALE)

    captcha = captchaSolver.solveCaptcha(image)[0]

    response = {
        "captcha": captcha
    }

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)