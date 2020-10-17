import os
from flask import Flask, request, abort, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    # region Configration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasker.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # endregion

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    def paginaite_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = QUESTIONS_PER_PAGE+start
        current_items = [selected.format() for selected in selection]
        return current_items[start:end]

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        selection = Category.query.order_by(Category.id).all()
        All_Categories = [category.format() for category in selection]
        if len(selection)==0:
            abort(404)
        else:
            categories = {}
            for category in All_Categories:
                categories['{}'.format(category['id'])] = category['type']
            return jsonify({
                "success": True,
                "categories": categories
                })

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions', methods=['GET'])
    def get_all_questions():
        selection = Question.query.order_by(Question.id).all()
        total_questions = len(selection)
        questions = paginaite_questions(request, selection)
        if len(questions) == 0:
            abort(404)
        else:
            query_categories = Category.query.all()
            All_Categories = [category.format() for category in query_categories]
            categories = {}
            for category in All_Categories:
                categories['{}'.format(category['id'])] = category['type']
            current_category = None
            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": total_questions,
                "categories": categories,
                "current_category": current_category
                })
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question_to_delete = Question.query.filter_by(id=question_id).one_or_none()
        if question_to_delete is None:
            abort(404)
        else:
            question_to_delete.delete()
            return jsonify({
                "success":True,
                "id": question_to_delete.id
                })

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)
            search = body.get('search', None)
            if search:
                questions_query = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search))).all()
                questions = paginaite_questions(request, questions_query)
                total_questions = len(questions_query)
                return jsonify({
                    "success": True,
                    "questions": questions,
                    "total_questions":total_questions,
                    "current_category":None
                })
            else:
                new_Question = Question(
                    new_question, new_answer, new_category, new_difficulty)
                new_Question.insert()
                return jsonify({
                    "success": True,
                    "question": new_Question.question,
                    "answer":new_Question.answer,
                    "difficulty":new_Question.difficulty,
                    "category":new_Question.category
                })
        except:
            abort(422)
    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)
            search = body.get('search', None)
            if search:
                questions_query = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search))).all()
                questions = paginaite_questions(request, questions_query)
                total_questions = len(questions_query)
                return jsonify({
                    "success": True,
                    "questions": questions,
                    "total_questions":total_questions,
                    "current_category":None
                })
            else:
                new_Question = Question(
                    new_question, new_answer, new_category, new_difficulty)
                new_Question.insert()
                return jsonify({
                    "success": True,
                    "question": new_Question.question,
                    "answer":new_Question.answer,
                    "difficulty":new_Question.difficulty,
                    "category":new_Question.category
                })
        except:
            abort(422)
    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            selection = Question.query.filter(
                Question.category == str(category_id)).all()
            if selection[0] is None:
                abort(404)
            else:
                questions = [question.format() for question in selection]
                query_categories = Category.query.all()
                total_questions = len(selection)
                category = Category.query.filter(Category.id==category_id).one_or_none()
                currentCategory = category.format()
                return jsonify({
                    "success": True,
                    "questions": questions,
                    "totalQuestions": total_questions,
                    "current_category": currentCategory
                    })
        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def play():
        # body = request.get_json()
        # previousQuestions = body.get('previousQuestions',None)
        # categories = body.get('categories',None)
        # selection = Question.query.filter(Question.question != previousQuestions).all()
        # current_question = (random.choice(selection)).format()
        # return jsonify({"previous id": question_id,
        #                 "new question": post_question})
        return jsonify({})
    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    # region Error Handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource Not Found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
            }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method Not Allowed"
            }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
            }), 400
    # endregion

    return app
