from flask import Flask, Blueprint

from routes import user, auth, business, reviews, admin

app = Flask(__name__)

app.register_blueprint(user.user, url_prefix='/users')
app.register_blueprint(auth.auth, url_prefix='/auth')
app.register_blueprint(business.business, url_prefix='/businesses')
app.register_blueprint(reviews.review, url_prefix='/reviews')
app.register_blueprint(admin.administrator, url_prefix='/administrator')

@app.route('/')
def hello_world():
    return 'Ok'