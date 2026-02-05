# python fastAPI練習  
郵便番号を打つことで住所の取得が可能  
数字7桁のみ受け付けるようにバリデーションを実装
# 外部APIの利用について
本プロジェクトでは以下の外部APIを利用しています  
- [zipcode](https://zipcloud.ibsnet.co.jp/)
- [zipcodeAPI利用規約](https://zipcloud.ibsnet.co.jp/rule/api)


# 環境変数の準備
cp .env.sample .env  
その後、例のように値を入れてください  
# コンテナの起動  
docker compose build  
docker compose up  
http://127.0.0.1:8000/docs  
Dockerfile,docker-compose.yml,.envとかを編集したらbuild  
# 所感
動作確認用のswaggerを立ち上げるのに苦労した  
IPv6とIPv4の競合？でlocalhostでできないことを何とかするのに苦労した

# 今日学んだこと
dockerの環境構築名前空間の衝突  
ctrl + @, ctrl + 1これ便利すぎる  
ni ファイル名  
cp コピー元 コピー先  
.env ファイルの参考として.env.sampleを作成しておく,env.sampleにはAPIキーは直接書かないあくまで例だけ  
rm 削除したいファイル名