from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64))
    phone = db.Column(db.String(32))



class Bill(db.Model):
    __tablename__ = "bill"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gmtCreate = db.Column(db.DateTime)
    gmtModified = db.Column(db.DateTime)
    desc = db.Column(db.String(128))
    usdChange = db.Column(db.String(128))
    ccChange = db.Column(db.String(128))
    ethChange = db.Column(db.String(128))
    carbonScore = db.Column(db.String(128))
    accountId = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('Account', backref='bills')


class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accountNumber = db.Column(db.String(64))
    eth = db.Column(db.String(128))
    usd = db.Column(db.String(128))
    cc = db.Column(db.String(128))
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='account')


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itemName = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.Text)


class SubAccount(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currencyNumber = db.Column(db.String(64))
    currencyAddress = db.Column(db.String(1024))
    currencyName = db.Column(db.String(64))
    currencyBalance = db.Column(db.String(64))


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(64))
