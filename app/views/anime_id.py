from flask import Blueprint, request
from app.services.animes_service import Animes
from app.services.errors_service import NotFoundError, InvalidKeysError

bp_anime_id = Blueprint('anime_id', __name__, url_prefix='/api')

@bp_anime_id.get('/animes/<int:anime_id>')
def filter(anime_id):
    Animes.create_database()
    try:
        output = Animes.get_single_anime(anime_id)
        return output
    except NotFoundError as err:
        return err.message

@bp_anime_id.patch('/animes/<int:anime_id>')
def update(anime_id):
    Animes.create_database()
    data = request.get_json()
    try:
        Animes.check_keys(data)
        Animes.update_anime(anime_id, data)

        output = Animes.get_single_anime(anime_id)

        return output, 200
    except NotFoundError as err:
        return err.message
    except InvalidKeysError as err:
        return err.message

@bp_anime_id.delete('/animes/<int:anime_id>')
def delete(anime_id):
    Animes.create_database()
    
    try:
        Animes.get_single_anime(anime_id)       
        Animes.delete_anime(anime_id)
        return '', 204
    except NotFoundError as err:
        return err.message