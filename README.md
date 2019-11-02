# Googleカレンダーにルーチンを登録

## requirement
```
$ pip3 install  google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 準備
1. APIの有効化
https://developers.google.com/calendar/quickstart/python?hl=ja
の`Enable The GOOGLE CALENDER API`をクリックして`DOWNLOAD CLIENT CONFIGURATION`から`credentials.json`をワーキングディレクトリにダウンロード
2. requirementをインストール
python3なのでpip3でインストール
3. カレンダーIDを確認する
calender_register関数内calendarIdが正しいか確認. カレンダーIDはカレンダーの設定内のカレンダーの統合欄に書いてある


## How To Use
mnb変数に登録するルーチンを入れる

最下部main関数に登録したい年, 月, 登録を始めるルーチンIDを入れて実行する

実行後に次回登録を始めるルーチンIDが出力されるのでメモしておく

登録するカレンダーを変更する場合は, calender_register関数内calendarIdを変更する
