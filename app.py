import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, session

import requests

#laod environment variables
load_dotenv()

app = Flask(__name__)

app.secret_key = 'supersecretkey'  # Change this for production

# Set your Spoonacular API key here
SPOONACULAR_API_KEY = os.getenv('API_KEY')

# Homepage route
@app.route('/')
def index():
    return render_template('index.html', ingredients=session.get('ingredients', []))

# Add ingredient route
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    ingredient = request.form['ingredient']
    if 'ingredients' not in session:
        session['ingredients'] = []
    session['ingredients'].append(ingredient)
    return redirect(url_for('index'))

# Fetch recipes based on ingredients
@app.route('/recipes')
def recipes():
    ingredients = session.get('ingredients', [])
    if not ingredients:
        return redirect(url_for('index'))

    # Spoonacular API call to fetch recipes
    ingredients_string = ','.join(ingredients)
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_string}&number=10&apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(url)
    recipes = response.json()

    return render_template('recipes.html', recipes=recipes)

# Recipe details route
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(url)
    recipe = response.json()
    return render_template('recipe_detail.html', recipe=recipe)

# Clear session (ingredients)
@app.route('/clear')
def clear_ingredients():
    session.pop('ingredients', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
