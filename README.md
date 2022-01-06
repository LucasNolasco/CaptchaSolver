# CaptchaSolver

Model to solve six character captchas. The code available on this repository is based on the example presented [here](https://keras.io/examples/vision/captcha_ocr/), which solves captchas with five characters. Besides the size of the captchas, the main difference in the code available here is that it applies morphological filtering to reduce the noise on the captcha images.

![Example of captcha used to train the model](data/captcha_dataset/1EbzUd.png)

## Dependencies

The dependencies for this repository are listed on the requirements file. To install them:

```
$ python -m pip install -r requirements.txt
```

## How to run

To run the API for the captcha solver model:

```
$ python api.py
```

It will start a server locally, using the port 5000. In order to test this server, just run the test script:

```
$ python test.py
```

This script will iterate through all images on data/captcha_dataset, making a request for the server using each one of them.

## Docker image

This repository also contains a docker image, which may facilitate the execution on a different environment. To build this image:

```
$ docker build -t captcha-api:latest -f Dockerfile .
```

After the image is built, you can start the server just running the image like this:

```
$ docker run -p 5000:5000 --name captcha-api captcha-api:latest
```

## Documentation

With the server running, the API documentation may be found on http://localhost:5000/apidocs (or any other base url where the server is running).