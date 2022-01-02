# 傳說小助理

Template Code for TOC Project 202
## 介紹
藉由一個簡單的小機器人，帶你認識傳說對決這款手遊

## 功能
1.玩法、角色、職業查詢\
2.每周限免英雄查詢\
3.小小心理測驗

## 環境
* ubuntu 18.04
* Python 3.6.9

## 技術
* Beautifulsoup4
* 到官網抓取每周限免英雄及所有英雄資料 

## 使用說明
* 隨時輸入「restart」可重頭開始
* 隨時輸入「back」可返回上一頁
* 輸入`介紹`可獲得遊戲相關介紹
    * 輸入`簡介`可獲得遊戲簡介
	* 輸入`特色`可獲得遊戲特色
	* 輸入`新手`可獲得新手需要的資訊
		* 輸入`容易上手英雄`可得知適合新手的英雄
		* 輸入`英雄定位`可得知遊戲個職業介紹
			* 輸入想得知的職業後選擇`位置介紹` `攻略影片` `英雄`可察看該職業相應資訊
* 輸入`英雄`可獲得英雄相關資訊
	* 輸入`周免英雄free`可得知當周限免英雄
	* 輸入`英雄介紹`後輸入`數字1~103`可查看該英雄資訊
* 輸入`檢測適合位置`可玩心理測驗，一共六道題目，最後結果為五路之一  


## 效果展示
![fsm](./img/IMG_20220102_210233.jpg)
![fsm](./img/IMG_20220102_204616.jpg)
![fsm](./img/IMG_20220102_210307.jpg)
![fsm](./img/IMG_20220102_210332.jpg)
![fsm](./img/IMG_20220102_210358.jpg)
![fsm](./img/IMG_20220102_210417.jpg)
![fsm](./img/IMG_20220102_210439.jpg)
![fsm](./img/IMG_20220102_210458.jpg)
![fsm](./img/IMG_20220102_210512.jpg)
![fsm](./img/IMG_20220102_210531.jpg)
![fsm](./img/IMG_20220102_215932.jpg)
![fsm](./img/IMG_20220102_210706.jpg)
![fsm](./img/IMG_20220102_210725.jpg)
![fsm](./img/IMG_20220102_210908.jpg)
![fsm](./img/IMG_20220102_211506.jpg)


## Setup

### Prerequisite
* Python 3.6
* Pipenv
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)


#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
![fsm](./img/fsm.png)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
