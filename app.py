from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import dropbox


app = Flask(__name__)

conn = psycopg2.connect("dbname=gloliwoe user=gloliwoe password=DzE9p8MVZgwbohsY4iXuO-R7tCmBr-TI host=fanny.db.elephantsql.com port=5432")
cur = conn.cursor()   

DROPBOX_ACCESS_TOKEN = 'sl.B2KLL0grckk8iUdJr6_mjtMmNA08sCMwPHQo-rHufWKBjX3TOR605i_Us5l9dPdxpbIIPJ3yrbXUhEBkHvxBc04v-1vOonhjz2KqrFVqyHo1WjmSlD6aRE-ovGi_4-oDGD2bOr0BTbtxY_Y'
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    recipe_name = request.form['recipe_name']
    ingredients = request.form['ingredients']
    instructions = request.form['instructions']
    cooking_time = request.form['cooking_time']
    difficulty_level = request.form['difficulty_level']
    meal_type = request.form['meal_type']
    cuisine_type = request.form['cuisine_type']
    photo = request.files['photo']

    response = dbx.files_upload(photo.read(), f'/photos/{photo.filename}')

    shared_link = dbx.sharing_create_shared_link(response.path_display).url
    cur.execute('INSERT INTO recipes (recipe_name, ingredients, instructions, cooking_time, difficulty_level, meal_type, cuisine_type, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (recipe_name, ingredients, instructions, cooking_time, difficulty_level, meal_type, cuisine_type, shared_link))
    conn.commit()

    return redirect(url_for('success'))


@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/recipe')
def recipe():
    cur = conn.cursor()
    cur.execute('SELECT id, recipe_name, ingredients, instructions, cooking_time, difficulty_level, meal_type, cuisine_type FROM recipes')
    items = cur.fetchall()
    cur.close()
    return render_template('display.html', items=items)

@app.route('/details/<int:item_id>')
def details(item_id):
    cur.execute('SELECT * FROM recipes where id = %s', (item_id,))
    item = cur.fetchone()
    return render_template('details.html', item=item)



if __name__ == '__main__':
    app.run(debug=True)



