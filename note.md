# 開發的筆記

### 常用cmd語法
啟動環境 C:\python\env\django_work\Scripts\activate.py
cd django_line

### 啟動網頁
python manage.py runserver

#### 變更資料庫設計時
python manage.py makemigrations
python manage.py migrate

### 相依套件
pip install psycopg
pip install dj-database-url==1.3.0
pip install psycopg2

### ngork步驟
1. 環境下執行 python manage.py runserver 8000
2. 另開一個cmd cd C:\python\ngrok
   然後 ngrok http 8000