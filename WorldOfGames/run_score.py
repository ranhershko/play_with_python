# from application import app
from flask import Flask, render_template
from MainScores import score_server


def on_web():
    app = Flask(__name__)
    file_score_name, file_score_answer = score_server()
    @app.route('/')
    def home():
        if file_score_answer.isdigit():
            return render_template(file_score_name, SCORE=file_score_answer)
        else:
            return render_template(file_score_name, ERROR=file_score_answer)
    # app.jinja_env.cache = {}
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.jinja_env.auto_reload = True
    app.run(host='0.0.0.0', port=80,)

