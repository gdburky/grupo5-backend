from flask import Flask
from flask_cors import CORS
from resources.posts import posts_api
from resources.people import person_api
from resources.messages import messages_api
from resources.responses import responses_api
from resources.subscriptions import subscriptions_api
from resources_g3.people import g3_person_api
from resources_g3.posts import g3_posts_api
from resources_g3.messages import g3_messages_api

# Flask settings
FLASK_SERVER_NAME = '0.0.0.0'
FLASK_DEBUG = False  # Do not use debug mode in production

app = Flask(__name__)
CORS(app)
app.register_blueprint(posts_api, url_prefix='/api')
app.register_blueprint(person_api, url_prefix='/api')
app.register_blueprint(messages_api, url_prefix='/api')
#app.register_blueprint(responses_api, url_prefix='/api')
#app.register_blueprint(subscriptions_api, url_prefix='/api')

app.register_blueprint(g3_person_api, url_prefix='/api/g3')
app.register_blueprint(g3_posts_api, url_prefix='/api/g3')
app.register_blueprint(g3_messages_api, url_prefix='/api/g3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001, threaded=True)
