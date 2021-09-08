from flask import Flask

def init_app(app: Flask):
    from app.views.animes import bp_animes
    app.register_blueprint(bp_animes)
    from app.views.anime_id import bp_anime_id
    app.register_blueprint(bp_anime_id)