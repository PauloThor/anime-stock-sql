from flask import Blueprint, request, jsonify
from app.services.animes_service import Animes
from app.services.errors_service import AlreadyExistsError, InvalidKeysError

bp_animes = Blueprint('animes', __name__, url_prefix='/api')

@bp_animes.post('/animes')
def get_create():
    data = request.get_json()

    try:        
        Animes.check_keys(data)
        Animes.create_database()
        Animes.verify_anime_exists(data['anime'])

        new_anime = Animes(
            anime = data['anime'],
            released_date = data['released_date'],
            seasons = data['seasons']
        )
        
        output = new_anime.insert()

        return jsonify(output), 201

    except InvalidKeysError as err:
        return err.message
    except AlreadyExistsError as err:
        return err.message      

@bp_animes.get('/animes')
def post_create():
    Animes.create_database()
    output = Animes.get_animes()

    return {'data': output}