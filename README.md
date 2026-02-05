# python fastAPI練習  


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