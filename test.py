import requests
import base64
import cv2
import glob

def main():
    for addr in glob.glob('data/captcha_dataset/*.png'):
        img = cv2.imread(addr)
        _, im_arr = cv2.imencode('.png', img)
        im_bytes = im_arr.tobytes()
        image_b64 = base64.b64encode(im_bytes).decode('utf-8')

        payload = {
            'image': image_b64
        }

        response = requests.post("http://localhost:5000/captcha", json=payload)
        # response = requests.post("https://captchasolver-uvk2pv2hja-ue.a.run.app/captcha", json=payload)

        if response.status_code == 200:
            ground_truth = addr.replace(".png", "")[-6:].lower()
            print("Correct: {0}, Predicted: {1}".format(ground_truth, response.json()['captcha']))
        elif response.status_code == 400 or response.status_code == 500:
            print(response.reason)


if __name__ == '__main__':
    main()