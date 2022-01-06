FROM python:3.8

WORKDIR /captcha
COPY requirements.txt requirements.txt
RUN apt update
RUN apt install -y libgl1-mesa-glx
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install -r requirements.txt

COPY models models
COPY schemas schemas
COPY api.py api.py
COPY captcha_inference.py captcha_inference.py 

ENTRYPOINT [ "python", "api.py" ]