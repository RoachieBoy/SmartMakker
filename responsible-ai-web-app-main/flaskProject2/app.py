from flask import Flask, render_template
from flask_cors import CORS
from blueprints.lyric_generator import lg

app = Flask(__name__)
app.register_blueprint(lg, url_prefix='/lyric_generator/')
CORS(app)


@app.route('/')
def hello_world():
    return render_template(r'index.html')


if __name__ == '__main__':
    app.run(debug=True)
