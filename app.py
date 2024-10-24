from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Spoonacular API details
API_KEY = '3475738d335446f48a890c2b34da7299'
API_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch_recipes', methods=['POST'])
def fetch_recipes():
    ingredients = request.form.get('ingredients')
    params = {
        'apiKey': API_KEY,
        'ingredients': ingredients,
        'number': 5  # Fetch 5 recipes
    }
    
    response = requests.get(API_URL, params=params)
    recipes = response.json()
    
    return render_template('results.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
