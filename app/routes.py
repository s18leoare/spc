from flask import current_app as app
from flask import render_template


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
