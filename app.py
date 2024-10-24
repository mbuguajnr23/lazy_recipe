import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, session

import requests

#laod environment variables
load_dotenv()

app = Flask(__name__)

# Spoonacular API details
api_key = os.getenv('API_KEY')
# app.secret_key = 'TBA'

@app.route('/')
def index():

    #get the list of ingredients from the session (or initialize it)
    return render_template('index.html', ingredients=session.get('ingredients', []))


@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    # ingredient = request.form.get('Ingredient')

    # #add the new ingedient to the session
    # if 'ingedients' not in session:
    #     session['ingredients'] = []

    # session['ingredients'].append(ingredient)

    # return redirect(url_for('index'))

    pass

@app.route('/recipes')

def fetch_recipes():
    ingredients = session.get('ingredients',[])
    
    if not ingredients:
        return redirect(url_for('index')) #Redirect to index if no ingredients are available
    
    #converts the ingredients to a comma-separated string for the API request
    ingredients_str = ','.join(ingredients)

    #fetch resipes from spoonacular API
    response = requests.get(
        f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_str}&number=10&apiKey={API_KEY}'
    )

    recipe = response.json()


    return render_template('recipe_detail.html', recipe=recipe)

app.route('/clear_ingredints')
def clear_ingredients():
    #clear the ingredients from the session
    session.pop('ingredients', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
