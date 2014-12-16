stream_twitter
==========
StreamAPIを用いてツイッターの情報を取得し、それをDBに格納します。  
その後、matplotlib,Mecab,Cabochaなどを用いて、その内容を調査します。  
  
動作環境  
------
Windows7  
Python2.7  
  
下記のアプリケーソンをインストール済み  
・Mecab（文字コードはUTF-8)  
・Cabocha  （Windowsの場合、0.66でないと動かないかもしれません）
  
下記のライブラリをインストール済み  
・python_twitter  
・python-dateutil  
・peewee  
・matplotlib  
・mecab-python  
  http://sourceforge.net/projects/mecab/files/mecab-python/  


使い方  
------
(1)Twitterの検索結果をDBに格納する  
  
    python twitter_stream.py consumer_key consumer_secret access_token_key access_token_secret  #総選挙,#衆院選,選挙
  
これにより、カレントディレクトリにtwitter_stream.sqliteが作成される  
  

(2)時間ごとのヒストグラムの作成  
  
    python twitter_db_hist.py "2014/12/14 9:00" "2014/12/14 22:00" 3600

この例だと12/14 9:00(日本時間では18:00)～12/14 22:00(日本時間では12/15 07:00)に3600秒毎のツイート数のヒストグラムを求める。
  
(3)頻出度する単語の抽出  

    python twitter_db_mecab.py "2014/12/14 9:00" "2014/12/14 22:00" > mecab.txt

この例だと12/14 9:00(日本時間では18:00)～12/14 22:00(日本時間では12/15 07:00)の単語の頻出頻度をmecab.txtに出力します  
  
(4)係受け解析により文節の係受けの頻度をしらべる  

    python twitter_db_cabocha.py "2014/12/14 9:00" "2014/12/14 22:00"  > cabocha.txt

この例だと12/14 9:00(日本時間では18:00)～12/14 22:00(日本時間では12/15 07:00)の係受けの結果をcabocha.txtに出力します  

