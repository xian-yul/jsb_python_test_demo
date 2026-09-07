import requests

from utils.mysqldb import MySQLClient

url = 'https://api.shop.eduwork.cn/api/index'
request = requests.get(url)
print(request.status_code)
db = MySQLClient()
users = db.query("SELECT * FROM reviews WHERE review_id = %s", (request.status_code,))
print(users)
