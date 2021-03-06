import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

 
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_get_paginated(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_get_categories(self):
        res = self.client().get('/categories/10')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'not found')

    # ************************
    # Get Questions
    # *************************


    def test_requesting_for_valid_page(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # # Test getting question with invalid page

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # # ************************
    # # Delete Quesiton
    # # *************************

    # Delete Question
    # test to delete existing q
    def test_delete_question(self):
        QID = 26
        res = self.client().delete(f'/questions/{QID}')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == QID).one_or_none()     
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], QID)
        self.assertEqual(question, None)

    #  Tes delete method with non exist question
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # # # ************************
    # # # Add Quesiton
    # # # *************************

     # Test adding new question

    def test_add_question(self):
        new_question = {
            'question':
            'Were Ross and Rachel on a Break?',
            'answer': 'Yes',
            'category': 1,
            'difficulty': 3
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # # Test not allowed action in creation of new question
    def test_405_if_question_creation_not_allowed(self):
        new_question = {
            'question':
            'Rachel left Ross a drunken voicemail confessing her feelings after Ross and Julie were about to take what big relationship step?',
            'answer': 'Get a cat together',
            'category': 1,
            'difficulty': 2
        }
        res = self.client().post('/questions/500', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # # # ************************
    # # # Search Quesiton
    # # # *************************

    def test_search_question(self):
        search_word = {'searchTerm': 'original'}
        res = self.client().post('/questions/search', json=search_word)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # # Review this! it works with empty string but not with unavailable string!!

    def test_422_if_question_doesnt_exist_in_search(self):
        search_word = {'searchTerm': ''}
        res = self.client().post('/questions/search', json=search_word)
        data = json.loads(res.data)
        # print('response = ', data['questions'])
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # ************************
    # Add Quesiton by Category
    # *************************

    def test_get_question_by_available_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])



    def test_404_get_question_by_unavialble_category(self):
        res = self.client().get('/categories/500/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()