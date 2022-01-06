from flask import Flask, request, redirect
from captcha_inference import CaptchaSolver
import base64
import numpy as np
import cv2
from flask_cors import CORS
from flasgger import Swagger, swag_from

app = Flask(__name__)
captchaSolver = CaptchaSolver('models/prediction_captcha_model.h5', 'models/num_to_char_model.h5')

app.config['SWAGGER'] = {
    'title': 'Captcha Solver',
    'description': 'API for captcha solving. It only works for captchas with 6 characters.',
    'version': '0.1.0',
}

# Default config (Source: https://github.com/flasgger/flasgger#customize-default-configurations)
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, config=swagger_config)
CORS(app)

@app.route("/captcha", methods=['POST'])
@swag_from(specs="schemas/captcha.yml", validation=True)
def solveCaptcha():
    captcha_request = request.get_json()

    im_b64 = captcha_request['image'].encode('utf-8')

    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    image = cv2.imdecode(im_arr, flags=cv2.IMREAD_GRAYSCALE)

    captcha = captchaSolver.solveCaptcha(image)[0]

    response = {
        "captcha": captcha
    }

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)