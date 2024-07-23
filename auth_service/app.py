from flask import Flask
from auth_routes import auth_blueprint
from my_database_lib import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')

@app.route('/auth/test')
def test():
    return "<p>Test successful</p>"

@app.route('/test')
def kuber():
    return"<h1> hi! its version 3 </h1>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
