import datetime
from flask_package import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)
    how_many = db.Column(db.Integer)
    u_price = db.Column(db.Integer)
    t_price = db.Column(db.Integer)
    remaining = db.Column(db.Integer)
    revenue = db.Column(db.Integer)
    image = db.Column(db.String(20), default='default.jpg')
    date = db.Column(db.DateTime, nullable=False, default=datetime.date)
    sales = db.relationship('Sales', backref='stock', lazy=True)

    def __repr__(self):
        return f"Inventory('{self.item_id}', '{self.u_price}', '{self.t_price}', '{self.how_many}', " \
               f"'{self.remaining}', '{self.date}')"


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id'), nullable=False)
    how_many = db.Column(db.Integer)
    u_price = db.Column(db.Integer)
    t_price = db.Column(db.Integer)
    profit = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.date)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20))
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=3):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.date.today)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    annotation = db.Column(db.String(150), nullable=False)
