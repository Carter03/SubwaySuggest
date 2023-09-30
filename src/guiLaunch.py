# from flask import request, Flask, render_template, redirect
# import signal
# import os
# import webbrowser

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# def OpenWeb():
#     app.config["TEMPLATES_AUTO_RELOAD"] = True
#     webbrowser.open('http://127.0.0.1:5000', new=1)
#     app.run(host='127.0.0.1', extra_files=['templates/index.html'])

# @app.route('/stopServer', methods=['GET'])
# def CloseWeb():
#     os.kill(os.getpid(), signal.SIGINT)

import eel

eel.init('utils')

def OpenWeb():
    eel.start('index.html')

def Reload():
    eel.reload()