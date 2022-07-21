# from crypt import methods
import os
from turtle import title
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
Initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

#set CORS response headers
@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
    )
    response.headers.add(
        "Access-Control-Allow-Origin", "*"
    )
    return response



# ROUTES
'''
Endpoint
    GET /drinks
        it is a public endpoint
        it contains only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]

        if not drinks:
            abort(404)

        return jsonify({
            "success": True,
            "drinks": drinks
        }),200

    except:
        abort(422)


'''
Endpoint
    GET /drinks-detail
        it requires the 'get:drinks-detail' permission
        it contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]

        if not drinks:
            abort(404)

        return jsonify({
            "success": True,
            "drinks": drinks
        }),200

    except:
        abort(422)


'''
Endpoint 
    POST /drinks
        it creates a new row in the drinks table
        it requires the 'post:drinks' permission
        it contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    body = request.get_json()
    if 'title' and 'recipe' not in body:
        abort(422)
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)
    try:
        # create a new drink object to be inserted to the database with form data
        new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        new_drink.insert()
        # sort database rows in descending order of id so as the get the largest(first) id
        latest_drink = Drink.query.order_by(Drink.id.desc()).first()

        return jsonify({
            'success': True,
            'drinks': latest_drink.long()
        }),200
 
    except:
        abort(422)

            

'''
Endpoint 
    PATCH /drinks/<id>
        <id> is the existing model id
        it responds with a 404 error if <id> is not found
        it updates the corresponding row for <id>
        it requires the 'patch:drinks' permission
        it contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    body = request.get_json()
    up_title = body.get('title', None)
    up_recipe = body.get('recipe', None)
    selected_drink = Drink.query.filter(Drink.id == id).one_or_none()
    if selected_drink is None:
        abort(404)
    else:
        try:
            # compare changes made, persist only updates/changes
            selected_drink.title = up_title if up_title != selected_drink.title else selected_drink.title
            selected_drink.recipe = json.dumps(up_recipe) if json.dumps(up_recipe) != selected_drink.recipe else selected_drink.recipe
            
            selected_drink.long()
            selected_drink.update()
            # ensure persistence by querying for exact drink to return
            drink = Drink.query.filter(Drink.id == id).one()
            return jsonify({
                "success": True,
                "drinks": [drink.long()]
            }),200
        except:
            abort(422)
'''
Endpoint 
    DELETE /drinks/<id>
        <id> is the existing model id
        it responds with a 404 error if <id> is not found
        it deletes the corresponding row for <id>
        it requires the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def remove_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    else:
        try:
            drink.delete()
            return jsonify({
                "success": True,
                "delete": id
            }), 200
        except:
            abort(422)

# Error Handling

'''
422 Error handler
    unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
404 Error handler
    resource not found
'''
@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
Error handler for AuthError
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


# ssl test for https urls
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', ssl_context=('localhost.pem', 'localhost-key.pem'), debug=True)