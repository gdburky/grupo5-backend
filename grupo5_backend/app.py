from flask import Flask

from resources.posts import posts_api


DEBUG = True
HOST = 80

app = Flask(__name__)
app.register_blueprint(posts_api)



if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST)
