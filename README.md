YoutubeConnect
====
<p align="center">
<img src="https://user-images.githubusercontent.com/12383342/200178641-3e3bb1f7-d32b-4262-b008-9b49ba1dbbd3.png" width="90%" />
</p>

## Description

Youtube の Live配信からMinecraft Serverにコマンドを送信します。  
また、CallBackメソッドを変更することで任意のサーバに対してHTTPリクエストを送信することができます。   

command フォルダの中身のClassを拡張することで送信内容を変更することができます。

### 取得できるイベント一覧:

* textMessage
    * 通常のチャットメッセージ
* superSticker
    * スーパースティッカー
* superChat
    * スーパチャット
* newSponsor
    * 新規メンバー登録
* giftRedemption
    * メンバーシップギフト受け取り
* giftPurchase
    * メンバーシップギフト送信

## Demo

なんかDemo動画か何か作って To赤石さん

## Requirement

Python 3

## Usage

pychat をもとに作成されています。

初めにConst.py の YOUTUBE_VIDEO_ID に  
対象の動画IDを入力します。(https://www.youtube.com/watch?v=XXXXXXXXXXX) XXXXXの部分

Youtubeメッセージを受信すると  
Commandパッケージ直下にある、Classが呼び出されます。

data format

<table>
  <tr>
    <th>name</th>
    <th>type</th>
    <th>remarks</th>
  </tr>
  <tr>
    <td>type</td>
    <td>str</td>
    <td>"superChat","textMessage","superSticker","newSponsor"</td>
  </tr>
  <tr>
    <td>id</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>message</td>
    <td>str</td>
    <td>emojis are represented by ":(shortcut text):"</td>
  </tr>
  <tr>
    <td>messageEx</td>
    <td>str</td>
    <td>list of message texts and emoji dicts(id, txt, url).</td>
  </tr>
  <tr>
    <td>timestamp</td>
    <td>int</td>
    <td>unixtime milliseconds</td>
  </tr>
  <tr>
    <td>datetime</td>
    <td>str</td>
    <td>e.g. "2019-10-10 12:34:56"</td>
  </tr>
    <td>elapsedTime</td>
    <td>str</td>
    <td>elapsed time. (e.g. "1:02:27") *Replay Only.</td>
  </tr>
  <tr>
    <td>amountValue</td>
    <td>float</td>
    <td>e.g. 1,234.0</td>
  </tr>
  <tr>
    <td>amountString</td>
    <td>str</td>
    <td>e.g. "$ 1,234"</td>
  </tr>
  <tr>
    <td>currency</td>
    <td>str</td>
    <td><a href="https://en.wikipedia.org/wiki/ISO_4217">ISO 4217 currency codes</a> (e.g. "USD")</td>
  </tr>
  <tr>
    <td>bgColor</td>
    <td>int</td>
    <td>RGB Int</td>
  </tr>
  <tr>
    <td>author</td>
    <td>object</td>
    <td>see below</td>
  </tr>
</table>

Structure of author object.
<table>
  <tr>
    <th>name</th>
    <th>type</th>
    <th>remarks</th>
  </tr>
  <tr>
    <td>name</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>channelId</td>
    <td>str</td>
    <td>*chatter's channel ID.</td>
  </tr>
  <tr>
    <td>channelUrl</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>imageUrl</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>badgeUrl</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>isVerified</td>
    <td>bool</td>
    <td></td>
  </tr>
  <tr>
    <td>isChatOwner</td>
    <td>bool</td>
    <td></td>
  </tr>
  <tr>
    <td>isChatSponsor</td>
    <td>bool</td>
    <td></td>
  </tr>
  <tr>
    <td>isChatModerator</td>
    <td>bool</td>
    <td></td>
  </tr>
</table>

### rawdata

```json
{
	"id": 1,
	"videoId": "XXXXXXXXXXX",
	"channelName": "Channnel Name",
	"userId": "32-character fixed-length UUID",
	"data": {
		"author": {
			"badgeUrl": "",
			"type": "",
			"isVerified": false,
			"isChatOwner": false,
			"isChatSponsor": false,
			"isChatModerator": false,
			"channelId": "000000000000000000000000",
			"channelUrl": "http://www.youtube.com/channel/UCqVDpXKLmKeBU_yyt_QkItQ",
			"name": "YouTube system message",
			"imageUrl": "https://yt3.ggpht.com/584JjRp5QMuKbyduM_2k5RlXFqHJtQ0qLIPZpwbUjMJmgzZngHcam5JMuZQxyzGMV5ljwJRl0Q=s66-c-k-c0x00ffffff-no-rj"
		},
		"type": "textMessage",
		"id": "variable length UUID",
		"timestamp": 1667061815386,
		"elapsedTime": "",
		"datetime": "2022-10-30 01:43:35",
		"message": "HELLO WORLD",
		"messageEx": [
			"HELLO WORLD"
		],
		"amountValue": 0,
		"amountString": "",
		"currency": "",
		"bgColor": 0
	}
}
```

## Install

`pip install -r requirements.txt`

## Run

`python client_main.py`

## Contribution

[Ai-Akaishi](https://github.com/Ai-Akaishi)

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[wakokara](https://twitter.com/@wakokara)

このプログラムは研究目的のためのものです。研究・教育用途のみにてお使いください。これらを利用したことにより生じた責任は負いかねます
