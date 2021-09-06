import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from auth  import *
from models import *

def create_app(test_config=None):
  app = Flask(__name__)
  CORS(app)
  migrate = Migrate(app, db)
  setup_db(app)

  PAGE = 3
  def paginate_questions(request, selection):
    nb = request.args.get('page', 1, type=int)
    first = (nb - 1) * PAGE
    last = first + PAGE
    nbQ = [question.format() for question in selection]
    q = nbQ[first:last]

    return q

  @app.route('/' , methods=['GET'])
  def hello():
    return render_template('index.html')

  def noPlatters():
        return jsonify({'success': True,'platters': 'There is no platter :('}), 200
  
  def error422():
    abort(422)

  def resPlatter(nPlatter, nbP):
    return jsonify({'success': True,'dishes': nPlatter,'total_dishs': nbP ,}), 200

  def dArea():
      return jsonify({
             'success': False,
              'message':"complete the Info. "
         }), 400

  def fArea():
      return jsonify({
             'success': True,
              'message':"Done "
         }), 200 


  def noOne():
    return jsonify({
             'success': False,
              'message':"Sorry there is no available "
         }), 409


  def taken_res(pers):
    return jsonify({
        'success': True,
        'reservation': pers
         }), 200


  def takenDetails():
      return jsonify({
             'success': True,
              'reservation_detail':'there is no res. taken '
         }), 200


  def resDetail(ntaken, nb):
    return jsonify({
             'success': True,
              'reservation_detail': ntaken,
              'total_reservations': nb,
         }), 200    



  def add():
    return jsonify({
              'success': True,
              'message':'Done '
           }), 200
  def errorAdd():
    return jsonify({
              'success': False,
              'message':"complete the Info. " 
           }), 400


  def incorrect():
    return jsonify({
              'success': False,
              'message':"incorrect one " 
           }), 400


  def updateD():
     return jsonify({
              'success': True,
              'message':"Done " 
           }), 200

  @app.route('/menu/add', methods=['POST'])
  @requires_auth('post:dish')
  def make_one(jwt):
    try:
      js = request.get_json();
      getName = js.get('dish_name' , None);
      getCat = js.get('category' , None);
      getDes = js.get('description' , None);
      getPr = js.get('price' , None);

      if((getName) and (getCat) and (getDes) and (getPr)): 

          tmp =  Menu( dish_name= getName , category = getCat, description = getDes ,  price = getPr )
          tmp.insert()
          return add()
      else:
         return errorAdd()
    except:
      error422()

  @app.route('/book' , methods=['POST'])
  def take_booking():
    try:
      js = request.get_json();
      per = js.get('account' , None);
      tik = js.get('appointmentـTime' , None);
      pers = js.get('guest' , None);
      bo = js.get('chairs' , None);
      if((per) and (tik ) and (pers) and (bo)):
        nbBo = int(bo)
        area= Table.query.filter( Table.chairs_num == nbBo ).all()
        taken = Reservation.query.filter(Reservation.appointmentـTime == tik)
        takes =[]
        for tmp1 in taken:
            takes.append(tmp1.table_id)
        aera = None
        for tmp2 in area:
            if tmp2.id not in takes:
                area = tmp2.id
                break
        if area is None:
          return noOne()
        if((per) and (tik ) and (pers) and (area)):
          book =  Reservation(guest=pers , appointmentـTime= tik, table_id=area , account=per)
          book.insert()
          return fArea()
      else:
        return dArea()
    except:
      error422() 


  @app.route('/menu' , methods=['GET'])
  def get_platter_of_menu():
    try:
       all = Menu.query.all()
       nPlatter = paginate_questions(request , all)
       if not all:
          return noPlatters()
       nbPlatter = []
       for dish in all:
         nbPlatter.append({"id": dish.id ,"dish_name": dish.dish_name,"category": dish.category,
        "description" : dish.description,
        "price": dish.price
        })
       nbP = len(all)
       return resPlatter(nPlatter, nbP)
    except:
        error422()


  @app.route('/menu/<int:dish_id>/delete', methods=['DELETE'])
  @requires_auth('delete:dish')
  def delete_it(jwt , dish_id):
    try:
      tmp = Menu.query.get(dish_id)
      if not tmp :
        return incorrect()
      tmp.delete()
      return updateD()
    except:
      error422()   

  @app.route('/reservation-detail' , methods=['GET'])
  @requires_auth('read:reservations-details')
  def takenDetail(jwt):
    try:
      taken = Reservation.query.all()
      ntaken = paginate_questions(request , taken)
      if not taken :
        return takenDetails()

      every = []
      for tmp in taken:
        every.append({
        'id':tmp.id,
        'guest':tmp.guest,
        'table_id': tmp.table_id,
        'appointmentـTime': tmp.appointmentـTime
        })
      nb =  len(taken)
      return resDetail(ntaken, nb)
    except:
      error422()


  @app.route('/menu/<int:dish_id>/edit', methods=['PATCH'])
  @requires_auth('edit:dish')
  def change(jwt , dish_id):
    try:
      getD = Menu.query.get(dish_id); 
      if not getD :
        return incorrect()
      js = request.get_json();
      getName= js.get('dish_name' , None);
      getCat = js.get('category' , None);
      getDes = js.get('description' , None);
      getPr = js.get('price' , None);

      if getName :
       getD.dish_name = getName
      if getCat :
       getD.category = getCat
      if getDes :
       getD.description = getDes
      if getPr :
       getD.price = getPr

      getD.update()
      return updateD()
    except:
      error422()
      

  @app.route('/<string:user>/reservation' , methods=['GET'])
  @requires_auth('read:reservation')
  def the_taken(jwt , user):
      taken = Reservation.query.filter(Reservation.account == user).all()
      pers = []
      for tmp in taken:
        pers.append({
        'table_id': tmp.table_id,
        'appointmentـTime': tmp.appointmentـTime
        })
      return taken_res(pers)

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


  @app.errorhandler(AuthError)
  def process_AuthError(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response

  return app
app = create_app()

if __name__ == '__main__':
    app.run()