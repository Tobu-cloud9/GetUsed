FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip uninstall django-allauth
RUN pip install -r requirements.txt

# パッケージの更新確認
RUN apt-get -y update

#chromeブラウザのインストール
RUN apt-get install -y unzip
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable


# chromeドライバのインストール
RUN curl -OL https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip chromedriver
RUN mv chromedriver /usr/bin/chromedriver

COPY . /code/

EXPOSE 8000