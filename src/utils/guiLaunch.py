from flask import request, Flask, render_template
# import signal
import os
import webbrowser

app = Flask(__name__)
# app.app_context().push()

# reload = False

@app.route('/')
def index():
    # global reload
    # if reload:
    #     Flask.flash("reload")
    #     reload = False
    return render_template('index.html')

def OpenWeb():
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    webbrowser.open('http://127.0.0.1:5000', new=1)
    app.run(host='127.0.0.1', extra_files=['templates/index.html'])

# def Reload():
#     global reload
#     reload = True


# @app.route('/stopServer', methods=['GET'])
# def CloseWeb():
#     os.kill(os.getpid(), signal.SIGINT)