import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, session, flash
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')  # Use environment variable for security

# Get Spoonacular API key from environment variables
SPOONACULAR_API_KEY = os.getenv('API_KEY')

# # Check if API key is set
# if not SPOONACULAR_API_KEY:
#     raise ValueError("API_KEY not set in environment variables.")

# Homepage route
@app.route('/')
def index():
    ingredients = session.get('ingredients', [])
    return render_template('index.html', ingredients=ingredients)

# Add ingredient route
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    ingredient = request.form.get('ingredient')
    if ingredient:
        if 'ingredients' not in session:
            session['ingredients'] = []
        session['ingredients'].append(ingredient)
    else:
        flash("Please enter a valid ingredient.", "error")
    return redirect(url_for('index'))

# Fetch recipes based on ingredients
@app.route('/recipes')
def recipes():
    ingredients = session.get('ingredients', [])
    if not ingredients:
        flash("No ingredients added. Please add ingredients first.", "info")
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
    flash("Ingredients cleared.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
