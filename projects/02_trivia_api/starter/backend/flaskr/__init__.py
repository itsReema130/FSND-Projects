import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10 

def paginate_question(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  # DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  # DONE: Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
    return response
#   DONE: Create an endpoint to handle GET requests 
#   for all available categories.
  @app.route('/categories', methods=['GET'])
  def get_categories():

    categories = Category.query.order_by(Category.id).all()
    CategoryData = {}
    for category in categories:
      CategoryData[category.id] = category.type
    if (len(CategoryData) == 0):
      abort(404)
    return jsonify({
      'success': True,
      'categories': CategoryData
    })
#   DONE: Create an endpoint to handle GET requests for questions
  @app.route('/questions',methods=['GET'])
  def getQuestions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_question(request, selection)
       
        categories = Category.query.order_by(Category.id).all()
        catgs_dict = {cat.id: cat.type for cat in categories}      
        
        if len(current_questions) == 0:
                abort(404)
                 
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': None,
            'categories': catgs_dict 
        })

#   Done:Create an endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_specific_question(question_id):
     try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            print(question)
            if question is None:
                abort(404)
            Question.query.get(question_id).delete()
            return jsonify({
                "success": True,
                "deleted": question.id,
            })
     except:
      abort(422)

#   DONE:Create an endpoint to POST a new question, 
  @app.route('/questions', methods=['POST'])
  def create_question():
        body = request.get_json()
        add_question = body.get('question', None)
        add_answer = body.get('answer', None)
        add_category = body.get('category', None)
        add_difficulty = body.get('difficulty', None)

        if not (add_question and add_answer and add_difficulty
                and add_category):
            abort(
                400, {
                    'message': 'Please, Fill all the required fields'})

        try:
            # insert the new Q to the database
            question = Question(question=add_question,
                                answer=add_answer,
                                difficulty=add_difficulty,
                                category=add_category)
            question.insert()
            return jsonify(
                {'success': True,
                'created': question.id})
        except BaseException:
            # If anything went wrong, handle the 422 error
            abort(422)

# DONE:Create a POST endpoint to get questions based on a search term. 
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        try:
            if len(search_term) == 0:
                abort(404)
            if search_term:
                search_results = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                current_categories = list(
                    set(result.category for result in search_results))
                return jsonify({
                    'success': True,
                    'questions':
                    [question.format() for question in search_results],
                    'total_questions': len(search_results),
                    'current_category': current_categories
                })
        except :
            abort(422)

#   Done:Create a GET endpoint to get questions based on category.
  @app.route('/categories/<int:cat_id>/questions')
  def retrieve_questions_by_category(cat_id):

        selection = Question.query.order_by(Question.id).filter(Question.category == cat_id).all()
        current_questions = paginate_question(request, selection)
        categories = Category.query.order_by(Category.id).all()
        catgs_dict = {cat.id: cat.type for cat in categories}
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success':True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': None,
            'categories': catgs_dict
        })

#   Done: Create a POST endpoint to get questions to play the quiz.
  @app.route('/quizzes', methods=['POST'])
  def retrieve_questions_for_quiz():
        body = request.get_json()
        category_dict = body.get('quiz_category', None)
        prev_qs_list = body.get('previous_questions')

        if not category_dict:
            abort(422)

        cat_id = category_dict.get('id')
        if cat_id == 0:
            selection = Question.query.all()
        else:
            selection = Question.query.filter(Question.category == cat_id).all()
        current_questions = [question.format() for question in selection]
        question = None
        random.shuffle(current_questions)
        for q in current_questions:

            if q['id'] not in prev_qs_list:
                question = q

        return jsonify({
            'question': question
        })

#   DONE: Create error handlers for all expected errors 
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

  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

  @app.errorhandler(500)
  def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

  return app

if __name__ == "__main__":
    create_app().run()