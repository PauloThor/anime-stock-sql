class InvalidKeysError(Exception):
    def __init__(self, keys, *args, **kwargs):
        super().__init__(keys, *args, **kwargs)

        self.message = {
            "available_keys": [
                "anime",
                "released_date",
                "seasons"
            ],
            "wrong_keys_sended": keys
        }, 422        

class AlreadyExistsError(Exception):
    def __init__(self, anime, *args, **kwargs):
        super().__init__(anime, *args, **kwargs)

        self.message = {
            "error": f'anime {anime.title()} already exists'
        }, 422        

class NotFoundError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "Not Found"
        }, 404        
