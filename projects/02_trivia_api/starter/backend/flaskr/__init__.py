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
#   '''
#   DONE: Create an endpoint to handle GET requests 
#   for all available categories.
#   '''
  @app.route('/categories', methods=['GET'])
  def get_categories():

    categories = Category.query.all()
    CategoryData = {}
    for category in categories:
      CategoryData[category.id] = category.type

   
    if (len(CategoryData) == 0):
      abort(404)

  
    return jsonify({
      'success': True,
      'categories': CategoryData
    })

          


#   '''
#   DONE: Create an endpoint to handle GET requests for questions, 

  @app.route('/questions',methods=['GET'])
  def getQuestions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
       
        questions = Question.query.all()
        if len(questions) <= start:
                abort(404)
                 
        formatted_question = [question.format() for question in questions]
        return jsonify({
          'success': True,
          'questions':formatted_question[start:end],
          'total_questions':len(formatted_question)
        }) 



#   including pagination (every 10 questions). 
#   This endpoint should return a list of questions, 
#   number of total questions, current category, categories. 

#   TEST: At this point, when you start the application
#   you should see questions and categories generated,
#   ten questions per page and pagination at the bottom of the screen for three pages.
#   Clicking on the page numbers should update the questions. 
#   '''

#   '''
#   done:Create an endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_specific_question(question_id):
     try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            Question.query.get(question_id).delete()
            return jsonify({
                "success": True,
                "deleted": question.id,
            })


     except:
      abort(422)
      
#   TEST: When you click the trash icon next to a question, the question will be removed.
#   This removal will persist in the database and when you refresh the page. 
#   '''

#   '''
#   TODO:Create an endpoint to POST a new question, 
  @app.route('/questions', methods=['POST'])
  
  def create_question():
      print('expet1')
      new_question=Question(    
              body = request.json.get(),
              question = body()['question'],
              answer = body()['answer'],
              category = body()['category'],
              difficulty = body()['difficulty']
        )
      if ((request.json.get('question') == '') | (request.json.get('answer') == '') | (
                request.json.get('difficulty') == '') | (request.json.get('category') == '')):
            print('expet2')
            return abort(404)
      else:  
        try:
      
          new_question.insert()
          return jsonify({
                  "success": True,
                  "created": new_question.id,
              })
        except:
              print('expet3')
              abort(422)
          
        # body = request.get_json()
        # print(body)
        # new_question =body.get('question',None)
        # new_answer=body.get('answer',None)
        # new_category=body.get('category',None)
        # new_difficulty=body.get('difficulty',None)

        # try:
        #     QUESTION = Question(question=new_question, answer=new_answer, category=new_category, difficulty= new_difficulty) 
        #     QUESTION.insert()

        #     selection = Question.query.order_by(Question.id).all()
        #     current_question = paginate_question(request, selection)

        #     return jsonify({
        #       'success': True,
        #       'created': QUESTION.id,
        #       'Question': current_question,
        #       'total_questions': len(Question.query.all())
        #     })

        # except:
        #     abort(422)
# 
# 
# 
# 

#   which will require the question and answer text, 
#   category, and difficulty score.

#   TEST: When you submit a question on the "Add" tab, 
#   the form will clear and the question will appear at the end of the last page
#   of the questions list in the "List" tab.  
#   '''

#   '''
#   
# TODO:Create a POST endpoint to get questions based on a search term. 
#   It should return any questions for whom the search term 
#   is a substring of the question. 

#   TEST: Search by any phrase. The questions list will update to include 
#   only question that include that string within their question. 
#   Try using the word "title" to start. 
#   '''

#   '''
#   TODO:Create a GET endpoint to get questions based on category. 

#   TEST: In the "List" tab / main screen, clicking on one of the 
#   categories in the left column will cause only questions of that 
#   category to be shown. 
#   '''


#   '''
#   TODO: Create a POST endpoint to get questions to play the quiz. 
#   This endpoint should take category and previous question parameters 
#   and return a random questions within the given category, 
#   if provided, and that is not one of the previous questions. 

#   TEST: In the "Play" tab, after a user selects "All" or a category,
#   one question at a time is displayed, the user is allowed to answer
#   and shown whether they were correct or not. 
#   '''

#   '''
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
#   including 404 and 422. 
#   '''
  
#   including 404 and 422. 
#   '''
{"question":"how are you","answer":"good","category":"gratings","difficulty":"1"}