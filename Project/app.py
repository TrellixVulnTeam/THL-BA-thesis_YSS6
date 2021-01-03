from flask import Flask, render_template, url_for, request

app = Flask(__name__,static_folder='./static')

@app.route('/')
def demo():
    return render_template("demo.html")

@app.route('/prediction/',methods=['POST'])
def dataHandler():
    print(request.json)
    return 'hello world'

if __name__ == "__main__":
    app.run()