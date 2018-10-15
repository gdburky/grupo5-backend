from flask import Flask

from resources.posts import posts_api

# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_VALIDATE = True
RESTPLUS_ERROR_404_HELP = False


app = Flask(__name__)

app.config['SERVER_NAME'] = FLASK_SERVER_NAME
app.config['RESTPLUS_VALIDATE'] = RESTPLUS_VALIDATE
app.config['ERROR_404_HELP'] = RESTPLUS_ERROR_404_HELP

app.register_blueprint(posts_api)



if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
