from flask import Flask

from resources.posts import posts_api
from resources.people import person_api
from resources.messages import messages_api
from resources.responses import responses_api
from resources.subscriptions import subscriptions_api

# Flask settings
FLASK_SERVER_NAME = '0.0.0.0'
FLASK_DEBUG = False  # Do not use debug mode in production

app = Flask(__name__)

app.register_blueprint(posts_api, url_prefix='/api')
app.register_blueprint(person_api, url_prefix='/api')
app.register_blueprint(messages_api, url_prefix='/api')
app.register_blueprint(responses_api, url_prefix='/api')
app.register_blueprint(subscriptions_api, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=FLASK_DEBUG, port=5000)
