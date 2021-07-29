import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import APP
from models import setup_db, Movies, Actors, Link, db, db_drop_and_create_all

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = APP
        self.client = self.app.test_client

        self.database_name = "capstone_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant_token = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZ5SjJLZTA5dVMyaWZWZjZYUGNzaiJ9.eyJpc3MiOiJodHRwczovL25hcmF0LWF1dGguZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZDA4ZGYyYjcyYTlmMDA2YTI5NmY5MiIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyNzU0NzQ3MSwiZXhwIjoxNjI3NTU0NjcxLCJhenAiOiJTSFJUb01DWGhYZGF6eXN6anpWMUtMVVlkaGFxOEUxNyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.H2gwJdz5QINk4b1D5wATm8bU5_BJN4GJbrFTbJpQX0hY2k2Lk_K0pkzTp2cEvf5DdL17RQ2nW5_7ekDuDHkq0e-3BaP4FqE2B_339SP6oh3O3JMXZlL5gtFu3xrbzYPx7RCM8BiXIseZd5DpTlB59kPZUN4dLn67iaPTZM9VaRtN26QP6IrcEhynhFoHMdkDbtvNGeVfYD8e2RScp3uhqpHyOaPf-gheqlwYIBI2bse3hTp-JQhLmENEQ0xmFsxThdD4vM-9qc5a7AY7BHgR9ST2BBoQPScNZYZ0spLs4OVxxM_rR3pD_Ads0jnJmN_lSrjWBnD0QljRbtqtYg5QHQ'
        }

        self.casting_director_token = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZ5SjJLZTA5dVMyaWZWZjZYUGNzaiJ9.eyJpc3MiOiJodHRwczovL25hcmF0LWF1dGguZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMDI1Mzk3ODU0MWE2MDA3MWJlOTZmYyIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyNzU0NzQyOSwiZXhwIjoxNjI3NTU0NjI5LCJhenAiOiJTSFJUb01DWGhYZGF6eXN6anpWMUtMVVlkaGFxOEUxNyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.AXT3r_ApmQ0nZjHakizsGF4KtlybRGce05fJ99HSlqVZoU-Y6kJpV1IQiiVfFBDXG6SL-FgmmEVvbYNNGHVuv3HXgUMvs7GkapBb424drsrCxk7L9nsoeAOuh1q2UaB1FC2JRJbr40FRv7M2UowX2I_gE1MwOttVaaVzxOVGbVGN8NgDSDPaAOR8xPSumq1XIuJmn808ohs5ER3SeNlDwfurtUcMkyHZcmrCYb6TQBOqAbMY9G6FGso4QkTQuifKlI6J_0WV02RX2eP-iPugJ6Lg7wkxY02SvARUnQH9A4jgwGUaMBDyGeM9kn0npaCF3A1AfrGU5aXijmjnGx_SkQ'
        }

        self.executive_producer_token = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZ5SjJLZTA5dVMyaWZWZjZYUGNzaiJ9.eyJpc3MiOiJodHRwczovL25hcmF0LWF1dGguZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYjRiNjE5ZDFjNzUzMDA3MDkwMmExMiIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyNzU0NzE4NSwiZXhwIjoxNjI3NTU0Mzg1LCJhenAiOiJTSFJUb01DWGhYZGF6eXN6anpWMUtMVVlkaGFxOEUxNyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.HXvcHITnl7RznUZwEn3UQ5thrAi3wh_SRmo-NhsOtwzV7hRDKiey3uYL-raQDsKxMLKNXrH7l-N9w8wxKMYpRH8-RS4DMuxAnR97EWN0iGb3AcrvK7bZfFd7lf_0OPCSKfPRHT_WQZEpLMK8AAgF3vMXF4YzSs6C7OGTUzcpqOxnnLHKW04WoY44KOwIiBZuPzHDCCr0mu_P29am5eTA2NTof7MDuR3XzfF_63mRU_t9-u15Vekn87ONebW82PCXm90rkMgpIUaY_k55znHBnXyM3wdMMW8bQioE31TIzBWwGJLyPVjv4B_abCkIkNJnsJAp4upoVehwTUdXm9g5ZA'
        }

        self.test_movie = {
            'title': 'Very Good Movie 2',
            'release_date': '2021-01-29',
            'actor':2
        }

        self.update_movie = {
            'title': 'Excellent Movie',
            'rating':'5.0'
        }

        self.test_actor = {
            'name': 'John Doe',
            'age': '38',
            'gender': 'male',
            'movie': 3
        }

        self.update_actor = {
            'age': '40',
            'gender': 'non-binary'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            db_drop_and_create_all()

        actor1 = Actors(
            name="Jane Doe",
            age="32",
            gender="female"
        )
        actor2 = Actors(
            name="Jane Doe",
            age="32",
            gender="female"
        )
        actor3 = Actors(
            name="Jane Doe",
            age="32",
            gender="female"
        )
        movie1 = Movies(
            title="Very Good Movie",
            release_date="2021-02-02",
            rating=5.0,
        )
        movie2 = Movies(
            title="Very Good Movie",
            release_date="2021-02-02",
            rating=5.0,
        )
        movie3 = Movies(
            title="Very Good Movie",
            release_date="2021-02-02",
            rating=5.0,
        )
        db.session.add_all([actor1, actor2, actor3, movie1, movie2, movie3])
        db.session.commit()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # actors and movies POST endpoint tests

    def test_post_actors_success(self):
        res = self.client().post('/actors', headers=self.casting_director_token, json=self.test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_actors_fail(self):
        res = self.client().post('/actors', headers=self.casting_assistant_token, json=self.test_actor)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_post_movies_success(self):
        res = self.client().post('/movies', headers=self.executive_producer_token, json=self.test_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movies_fail(self):
        res = self.client().post('/movies', headers=self.casting_assistant_token, json=self.test_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    #   movies and actors GET endpoint tests

    def test_get_movies_success(self):
        res = self.client().get('/movies', headers=self.casting_assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_fail(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    def test_get_movies_by_id_success(self):
        res = self.client().get('/movies/2', headers=self.casting_assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        print()

    def test_get_movies_by_id_fail(self):
        res = self.client().get('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        print()

    def test_get_actors_success(self):
        res = self.client().get('/actors', headers=self.casting_assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        print()

    def test_get_actors_fail(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_get_actors_by_id_success(self):
        res = self.client().get('/actors/2', headers=self.casting_assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        print()

    def test_get_actors_by_id_fail(self):
        res = self.client().get('/actors/100', headers=self.casting_assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        print()


    #   actors and movies PATCH endpoint tests

    def test_patch_actors_success(self):
        res = self.client().patch('/actors/2', headers=self.executive_producer_token, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_patch_actors_fail(self):
        res = self.client().patch('/actors/2', headers=self.casting_assistant_token, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_patch_movies_success(self):
        res = self.client().patch('/movies/2', headers=self.executive_producer_token, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_fail(self):
        res = self.client().patch('/movies/2', headers=self.casting_assistant_token, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    #   actors and movies DELETE endpoint tests

    def test_delete_actors_success(self):
        res = self.client().delete('/actors/1', headers=self.casting_director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_fail(self):
        res = self.client().delete('/actors/999', headers=self.casting_director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movies_success(self):
        res = self.client().delete('/movies/1', headers=self.executive_producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_fail(self):
        res = self.client().delete('/movies/999', headers=self.executive_producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

if __name__ == '__main__':
    unittest.main()