import pymysql
class database_test:
    def __init__(self):
        self.host = 'cluster01.proxysql.staging.internal'
        self.port = 6032
        self.user = 'adplatform_48113_v1_rw'
        self.password = 'Kv1yt0zHN1epZYGK4mLraIMQBDb5O8jc'
        self.database = 'lianmengtest'
        self.charset = 'utf8'

    def connect_database(self):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            charset=self.charset
        )
        return conn
    def close_database(self,conn):
        conn.close()
    def select_database(self,conn,sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def insert_database(self,conn,sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def update_database(self,conn,sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def delete_database(self,conn,sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()