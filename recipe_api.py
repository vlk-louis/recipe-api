from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    making_time = db.Column(db.String(100), nullable=False)
    serves = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(300), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']
    
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Recipe creation failed!", "required": required_fields}), 200
    
    new_recipe = Recipe(
        title=data['title'],
        making_time=data['making_time'],
        serves=data['serves'],
        ingredients=data['ingredients'],
        cost=data['cost']
    )
    db.session.add(new_recipe)
    db.session.commit()
    
    return jsonify({
        "message": "Recipe successfully created!",
        "recipe": [ 
            {
                "id": new_recipe.id,
                "title": new_recipe.title,
                "making_time": new_recipe.making_time,
                "serves": new_recipe.serves,
                "ingredients": new_recipe.ingredients,
                "cost": new_recipe.cost,
                "created_at": new_recipe.created_at,
                "updated_at": new_recipe.updated_at
            }
        ]
    }), 200


@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    result = [{
        "id": r.id,
        "title": r.title,
        "making_time": r.making_time,
        "serves": r.serves,
        "ingredients": r.ingredients,
        "cost": r.cost,
        "created_at": r.created_at,
        "updated_at": r.updated_at
    } for r in recipes]
    
    return jsonify({"recipes": result}), 200

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "Recipe details by id"}), 200

    return jsonify({
        "message": "Recipe details by id",
        "recipe": [
            {
                "id": recipe.id,
                "title": recipe.title,
                "making_time": recipe.making_time,
                "serves": recipe.serves,
                "ingredients": recipe.ingredients,
                "cost": recipe.cost,
                "created_at": recipe.created_at,
                "updated_at": recipe.updated_at
            }
        ]
    }), 200


@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "Recipe not found!"}), 200
    
    data = request.get_json()
    for key, value in data.items():
        setattr(recipe, key, value)
    db.session.commit()
    
    return jsonify({
        "message": "recipe successfully updated!",
        "recipe": {
            "id": recipe.id,
            "title": recipe.title,
            "making_time": recipe.making_time,
            "serves": recipe.serves,
            "ingredients": recipe.ingredients,
            "cost": recipe.cost,
            "created_at": recipe.created_at,
            "updated_at": recipe.updated_at
        }
    }), 200

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "recipe not found!"}), 200
    
    db.session.delete(recipe)
    db.session.commit()
    
    return jsonify({"message": "recipe successfully deleted!"}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "not found!"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
