from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')


@app.route('/outerwear/')
def outerwear():
    return render_template('outerwear.html')


@app.route('/accessories/')
def accessories():
    return render_template('accessories.html')
