from flask import Flask, render_template, url_for, request
import json

app = Flask(__name__,static_folder='./static')

@app.route('/')
def demo():
    return render_template("demo.html")

@app.route('/prediction')
def dataHandler():
    return 'hello world'