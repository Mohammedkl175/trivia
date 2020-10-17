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
        self.database_path = "postgresql://{}@{}/{}".format('postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """ The test function get all categories

    Returns:
       succeful response  
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
        
    """ The test function get category by id

    Returns:
       404 response  
    """
    def test_404_sent_get_category_by_id(self):
        res=self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Resource Not Found')

    """ The test function get all questions

    Returns:
       succeful response  
    """
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],None)

    """ The test function get questions by valid page

    Returns:
       404 response  
    """
    def test_404_sent_requesting_beyond_valid_page(self):
        res=self.client().get('/questions?page=100',json={'category':'4'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Resource Not Found')

    """ The test function search question/s by correct data

    Returns:
       succeful response  
    """
    def test_search_question_with_correct_data(self):
        res = self.client().post('/questions/search',json={'searchTerm':'Hematology is a branch'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    """ The test function search question/s by incorrect data

    Returns:
       succeful response  
    """
    def test_search_question_with_incorrect_data(self):
        res = self.client().post('/questions/search',json={'searchTerm':'kgkjgkjgk'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(len(data['questions']),0)

    """ The test function create question by valid URL

    Returns:
       succeful response  
    """
    def test_create_question(self):
        res = self.client().post('/questions',json={'question':'What is your name','answer':'Mohammed','category':'4','difficulty':4})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    """ The test function create question by invalid URL

    Returns:
       405 response  
    """
    def test_405_create_question_with_missing_data(self):
        res = self.client().post('/questions',json={'answer':'Mohammed','category':'4','difficulty':4})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Method Not Allowed')

    """ The test function delete question by correct id

    Returns:
       succeful response  
    """
    def test_delete_question_with_correct_id(self):
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['id'],6)

    """ The test function delete question by incorrect id

    Returns:
       404 response  
    """
    def test_404_delete_question_with_incorrect_id(self):
        res = self.client().delete('/questions/20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Resource Not Found')

    """ The test function get questions by correct category Id

    Returns:
       success response  
    """
    def test_get_questions_by_correct_category_id(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    """ The test function get questions by incorrect category Id

    Returns:
       404 response  
    """
    def test_404_get_questions_by_incorrect_category_id(self):
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Resource Not Found')

    """ The test function get question randomly at giving category

    Returns:
       succeful response  
    """
    def test_play(self):
        res = self.client().post('/quizzes',json={"quiz_category":{"type":"Art","id":2},"previous_questions":[6]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['question']))

    """ The test function get question randomly at giving category with missing data

    Returns:
       405 response  
    """
    def test_play_with_invalid_url(self):
        res = self.client().post('/quizzes',json={"previous_questions":[6]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Method Not Allowed')
    
if __name__ == "__main__":
    unittest.main()