from flask import Flask, render_template
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def OpenWeb():
    webbrowser.open('http://127.0.0.1:5000', new=1)
    app.run(host='127.0.0.1')

# OpenWeb()