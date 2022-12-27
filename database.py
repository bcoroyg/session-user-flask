import pymysql
from config import config

cfg = config['development']

config = {
    "user": cfg.MYSQL_USER,
    "password": cfg.MYSQL_PASSWORD,
    "host": cfg.MYSQL_HOST,
    "db": cfg.MYSQL_DB,
    "port": cfg.MYSQL_PORT
}


def connectdb():
    return pymysql.connect(**config)
