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


def create_user(email, password):
    connect = connectdb()
    with connect.cursor() as cursor:
        cursor.execute("INSERT INTO user(email, password) VALUES (%s, %s)", (email, password))
        connect.commit()
        connect.close()
        
def get_user_by_email(email):
    connect = connectdb()
    user = None
    with connect.cursor() as cursor:
        cursor.execute("SELECT email, password FROM user WHERE email=%s", (email))
        user = cursor.fetchone()
        connect.close()
        return user

#if __name__ == '__main__':
    #print(get_user_by_email("email@correo.com"))
