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

    """ App Configrations  
    """
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

    """ Register functions to be run after each request
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """ The function paginait questions by 10 qyestions per page
    
    Args:
       request: request sent by endpoint
       selection: list of selected questions 

    Returns:
       list of 10 questions per page  
    """
    def paginaite_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = QUESTIONS_PER_PAGE+start
        current_items = [selected.format() for selected in selection]
        return current_items[start:end]

    """ Endpoint with GET method to get all cetegories
    
    Args:
       /categories: HTTP Response (URL)
       methods=['GET']: HTTP Response (Method)

    Raises:
       abort(404): if categories not founded 

    Returns:
       jsonify(success,categories)  
    """
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

    """ Endpoint with GET method to get all questions
    
    Args:
       /questions: HTTP Response (URL)
       methods=['GET']: HTTP Response (Method) 

    Raises:
       abort(404): if questions not founded 

    Returns:
       jsonify(success,questions,total_questions,categories)  
    """
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

    """ Endpoint with DELETE method to delete question by its Id
    
    Args:
       /questions/<int:question_id>: HTTP Response (URL)
       methods=['DELETE']: HTTP Response (Method)

    Raises:
       abort(404): if question to delete not founded  

    Returns:
       jsonify(success,id)  
    """
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

    """ Endpoint with POST method to create new question
    
    Args:
       /questions: HTTP Response (URL)
       methods=['POST']: HTTP Response (Method)

    Raises:
       abort(422): unable to process the contained instructions  

    Returns:
       jsonify(success,question,answer,difficulty,category)  
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        if (new_question is None or new_answer is None or new_difficulty is None or new_category is None):
            abort(405)
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

    """ Endpoint with POST method to search for question/s.
    
    Args:
       /questions/search: HTTP Response (URL)
       methods=['POST']: HTTP Response (Method)

    Raises:
       abort(422): unable to process the contained instructions  

    Returns:
       jsonify(success,questions,total_questions,difficulty,category)  
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            search = body.get('searchTerm',' ')
            questions_query = Question.query.filter(
                Question.question.ilike('%{}%'.format(search))).all()
            questions = paginaite_questions(request,questions_query)
            total_questions = len(questions_query)
            current_category = [question['category'] for question in questions]
            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions":total_questions,
                "current_category": current_category
                })
        except:
            abort(422)

    """ Endpoint with GET method to get questions by thier category
    
    Args:
       /categories/<int:category_id>/questions: HTTP Response (URL)
       methods=['GET']: HTTP Response (Method)

    Raises:
       abort(404): if question to delete not founded 

    Returns:
       jsonify(success,questions,total_questions,current_category)  
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        selection = Question.query.filter(Question.category == str(category_id)).all()
        if len(selection)==0:
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
                "total_questions": total_questions,
                "current_category": currentCategory
                })

    @app.route('/quizzes', methods=['POST'])
    def play():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')

        if quiz_category['id'] == 0:
            available_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
            available_questions = Question.query.filter(Question
            .category==str(quiz_category['id'])
            ,Question.id.notin_(previous_questions)).all()

        if len(available_questions)==0:
            question = None
        else:
            current_question = random.choice(available_questions)
            question = current_question.format()
        return jsonify({
            "success":True,
            "question":question
        })

    """ Endpoints with error handler to return specific data about error
    
    Args:
       404: Resource Not Found
       422: unprocessable
       405: Method Not Allowed
       400: Bad Request

    Returns:
       jsonify(success,error,message)  
    """
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
