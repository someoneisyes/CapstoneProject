import os
from flask import (
    Flask,
    render_template,
    request,
    abort,
    jsonify,
    Response,
    flash,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import json

from models import (
    setup_db,
    db,
    Movies,
    Actors,
    Link,
    db_drop_and_create_all
)
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
     uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this funciton will add one
    '''

    # db_drop_and_create_all()

    migrate = Migrate(app, db)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def temp():
        return 'hello world'

    # GET ENDPOINTS

    # movies GET endpoint

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movies.query.order_by(Movies.id).all()
        format_movie = [format_movie.format() for format_movie in movies]

        if len(movies) == 0:
            abort(404)
        try:
            return jsonify({
                'success': True,
                'movies': format_movie,
                'total_movies': len(movies),
            }), 200
        except BaseException:
            abort(422)

    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def get_movie_by_id(token, movie_id):
        movie = Movies.query.get(movie_id)

        if movie is None:
            abort(404)

        # actors that starred in this movie.
        actors = [movie.actors[actor].name for actor in range(
            len(movie.actors))]

        try:
            return jsonify({
                'success': True,
                'details': movie.format(),
                'actors': actors,
            }), 200
        except BaseException:
            abort(422)

    # actors GET endpoint

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actors.query.order_by(Actors.id).all()
        format_actor = [format_actor.format() for format_actor in actors]

        if len(actors) == 0:
            abort(404)
        try:
            return jsonify({
                'success': True,
                'movies': format_actor,
                'total_actors': len(actors)
            }), 200
        except BaseException:
            abort(422)

    @app.route('/actors/<int:actor_id>')
    @requires_auth('get:actors')
    def get_actor_by_id(token, actor_id):
        actor = Actors.query.get(actor_id)

        if actor is None:
            abort(404)
            
        # movies that this actor starred in.
        movies = [actor.movies[movie].title for movie in range(
            len(actor.movies))]

        try:
            return jsonify({
                'success': True,
                'details': actor.format(),
                'movies': movies,
            }), 200
        except BaseException:
            abort(422)

    # POST ENDPOINTS

    # movies POST endpoint

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(token):
        try:
            data = request.get_json()
            new_movie = Movies(
                title=data.get('title'),
                release_date=data.get('release_date'),
                rating=data.get('rating')
            )
            actor_id = data.get('actor')
            actor = Actors.query.get(actor_id)

            new_movie.insert()

            if actor is not None:
                actor.movies.append(new_movie)
                db.session.commit()

            print('Movies: ' + new_movie.title)

            return jsonify({
                'success': True
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    # actors POST endpoint

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(token):
        try:
            data = request.get_json()
            new_actor = Actors(
                name=data.get('name'),
                age=data.get('age'),
                gender=data.get('gender'),
            )
            movie_id = data.get('movie')
            movie = Movies.query.get(movie_id)

            new_actor.insert()

            if movie is not None:
                movie.actors.append(new_actor)
                db.session.commit()

            print('Actors: ' + new_actor.name)

            return jsonify({
                'success': True
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    # PATCH ENDPOINTS

    # movies PATCH endpoint

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, movie_id):

        movie = Movies.query.get(movie_id)
        data = request.get_json()

        if movie is None:
            abort(404)

        try:
            movie.title = data.get('title', movie.title)
            movie.release_date = data.get('release_date', movie.release_date)
            movie.rating = data.get('rating', movie.rating)

            movie.update()

            return jsonify({
                'success': True
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    # actors PATCH endpoint

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(token, actor_id):

        actor = Actors.query.get(actor_id)
        data = request.get_json()

        if actor is None:
            abort(404)

        try:
            actor.name = data.get('name', actor.name)
            actor.age = data.get('age', actor.age)
            actor.gender = data.get('gender', actor.gender)

            actor.update()

            return jsonify({
                'success': True
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    # DELETE ENDPOINTS

    # movies DELETE endpoint

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):

        movie = Movies.query.get(movie_id)

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    # actors DELETE endpoint

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):

        actor = Actors.query.get(actor_id)

        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                'success': True
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    # Error handlers

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden request"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "something went wrong"
        }), 500

    @app.errorhandler(AuthError)
    def autherror(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
