from flask import Flask

from resources.posts import posts_api

# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True  # Do not use debug mode in production

app = Flask(__name__)

app.config['SERVER_NAME'] = FLASK_SERVER_NAME

app.register_blueprint(posts_api)

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
