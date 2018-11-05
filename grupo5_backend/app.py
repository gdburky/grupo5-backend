from flask import Flask

from resources.posts import posts_api
from resources.people import person_api
from resources.messages import messages_api
from resources.responses import responses_api
from resources.subscriptions import subscriptions_api

# Flask settings
FLASK_SERVER_NAME = 'charette14.ing.puc.cl'
FLASK_DEBUG = False  # Do not use debug mode in production

app = Flask(__name__)

app.config['SERVER_NAME'] = FLASK_SERVER_NAME


app.register_blueprint(posts_api, url_prefix='/api')
app.register_blueprint(person_api, url_prefix='/api')
app.register_blueprint(messages_api, url_prefix='/api')
app.register_blueprint(responses_api, url_prefix='/api')
app.register_blueprint(subscriptions_api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
