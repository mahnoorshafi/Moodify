from flask_debugtoolbar import DebugToolbarExtension

from views import app
from model import connect_to_db

if __name__ == '__main__':
    app.secret_key = 'SECRETSECRETSECRET'
    app.debug = False
    connect_to_db(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host = '0.0.0.0')