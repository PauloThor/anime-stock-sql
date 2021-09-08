from flask import jsonify
from app.services.database_service import Database
from .errors_service import AlreadyExistsError, InvalidKeysError

class Animes:
    
    def __init__(self, anime, seasons, released_date):
        self.anime = anime.title()
        self.seasons = seasons
        self.released_date = released_date        
        self.cur = None
        self.conn = None


    @staticmethod
    def create_database():
        db = Database()
        db.connect()        

        db.execute("""
        CREATE TABLE IF NOT EXISTS animes (
            id BIGSERIAL PRIMARY KEY,
            anime VARCHAR(100) NOT NULL UNIQUE,
            released_date DATE NOT NULL,
            seasons INTEGER NOT NULL
        );
        """)

        db.close()

    @staticmethod
    def check_keys(data):
        keys_that_should_exist = ['anime', 'released_date', 'seasons']
        keys = data.keys()
        incorrect_keys = [key for key in keys if key not in keys_that_should_exist]        

        if len(incorrect_keys) > 0:
            raise InvalidKeysError(incorrect_keys)


    def insert(self):        

        db = Database()
        db.connect()

        insert_query = """
            INSERT INTO animes (anime, seasons, released_date) 
            VALUES (%s,%s,%s) RETURNING id
        """
        data_to_insert = (self.anime, self.seasons, self.released_date)
        data = db.execute(insert_query, data_to_insert)        

        db.close()      

        return {
            "id": data[0],
            "anime": self.anime,
            "released_date": self.released_date,
            "seasons": self.seasons
        }

    @staticmethod
    def verify_anime_exists(anime):
        all_animes = Animes.get_animes()
        print(all_animes)
        output = [item for item in all_animes if item['anime'] == anime.title()]

        if len(output) > 0:
            raise AlreadyExistsError(anime)

    @staticmethod
    def get_animes():
        db = Database()
        db.connect()

        db.execute("""
            SELECT * FROM animes
        """)

        output = db.get_data()

        db.close()

        return output

    @staticmethod
    def get_single_anime(anime_id):
        db = Database()
        db.connect()

        output = db.get_data_by_id(anime_id)

        db.close()

        return {"data": output}

    @staticmethod
    def update_anime(anime_id, data):
        db = Database()
        db.connect()

        keys = data.keys()            

        for key in keys:
            if key == 'anime':
                sql = """
                UPDATE animes
                SET anime = %s
                WHERE id = %s
                """
                params = (data['anime'].title(), anime_id)
                db.update(sql, params)
            if key == 'released_date':
                sql = """
                UPDATE animes
                SET released_date = %s
                WHERE id = %s
                """
                params = (data['released_date'], anime_id)
                db.update(sql, params)
            if key == 'seasons':
                sql = """
                UPDATE animes
                SET seasons = %s
                WHERE id = %s
                """
                params = (data['seasons'], anime_id)
                db.update(sql, params)

        db.close()

    @staticmethod
    def delete_anime(anime_id):
        db = Database()
        db.connect()

        sql = """
            DELETE FROM animes
            WHERE id = %s
            RETURNING *
        """

        params = (anime_id,)

        db.execute(sql, params)
