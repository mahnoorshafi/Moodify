from flask_debugtoolbar import DebugToolbarExtension

from views import app

if __name__ == '__main__':
    app.secret_key = 'SECRETSECRETSECRET'
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host = '0.0.0.0')