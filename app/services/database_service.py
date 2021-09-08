import psycopg2 as pg2
from app.services.errors_service import NotFoundError

class Database:
    def __init__(self):
        self.db = 'animes'
        self.username = 'paulo'
        self.password = '1234'
        self.cur = None
        self.conn = None

    def connect(self):
        self.conn = pg2.connect(host='localhost', database=self.db, user=self.username,
        password=self.password)
        self.cur = self.conn.cursor()

    def execute(self, query, args = None):
        output = 0
        if not args:
            self.cur.execute(query)
        else:
            self.cur.execute(query, args)
            output = self.cur.fetchone()            
        self.conn.commit()
        return output

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_data(self):
        getting_data = self.cur.fetchall()
        FIELDNAMES = ["id", "anime", "released_date", "seasons"]
        processed_data = [dict(zip(FIELDNAMES, row)) for row in getting_data]
        self.conn.commit()

        return processed_data

    def get_data_by_id(self, id):
        sql = """
            SELECT * FROM animes
            WHERE id = %s
        """
        
        self.cur.execute(sql, (id,))

        getting_data = self.cur.fetchall()
        FIELDNAMES = ["id", "anime", "released_date", "seasons"]
        processed_data = [dict(zip(FIELDNAMES, row)) for row in getting_data]
        self.conn.commit()

        if len(processed_data) == 0:
            raise NotFoundError

        return processed_data

    def update(self, query, args = None):        
        self.cur.execute(query, args)
        
        self.conn.commit()