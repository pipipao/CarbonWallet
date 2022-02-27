from flask import Flask, render_template, redirect, request, session, url_for, g
from flask_sqlalchemy import SQLAlchemy
from decorators import login_required

import config
from exts import db

app = Flask(__name__)
app.config.from_object(config)
# db.init_app(app)
db = SQLAlchemy(app)
from models import *

db.drop_all()
db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('user_id'):
            return redirect(url_for('account'))
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username == username, User.password == password).first()
    if user:
        session['user_id'] = user.id
        session.permanent = True
        return redirect(url_for('account'))
    return redirect(url_for('register'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username == username).first()
    if user:
        return 'Please select another username'
    user = User(username=username, password=password)
    account = Account(eth='1', usd='1000', cc='1500')
    db.session.add(user)
    db.session.add(account)
    db.session.commit()
    user.account.append(account)
    db.session.commit()
    return redirect(url_for('login'))


@app.route("/home", methods=['GET'])
def home():
    return render_template('home.html')


@app.route("/bill", methods=['GET'])
@login_required
def bill():
    user = User.query.filter(User.id == session.get('user_id')).first()
    bills = user.account[0].bills
    return render_template('bill.html', bills=bills)


@app.route("/account", methods=['GET'])
@login_required
def account():
    user = User.query.filter(User.id == session.get('user_id')).first()
    account = user.account[0]
    eth = float(account.eth)
    cc = float(account.cc)
    usd = float(account.usd)
    vcc = int(cc * 2)
    veth = int(eth * 2000)
    vusd = int(usd)
    total = int(eth * 2000 + cc * 2 + usd)
    return render_template('account.html',
                           user=user, account=account,
                           total=int(eth * 2000 + cc * 2 + usd),
                           vcc=int(cc * 2),
                           veth=int(eth * 2000),
                           vusd=int(usd),
                           percent=int(vcc/total*100))


@app.route("/collections", methods=['GET'])
@login_required
def collections():
    return render_template('collections.html')


@app.route("/market", methods=['GET'])
@login_required
def market():
    return render_template('market.html')


@app.route("/addBill", methods=['GET', 'POST'])
@login_required
def addBill():
    if request.method == 'GET':
        return render_template('add_bill.html')
    print(request.form)
    desc = request.form.get('desc')
    cc = request.form.get('cc')
    usd = request.form.get('usd')
    eth = request.form.get('eth')
    if not cc:
        cc = 0
    if not eth:
        eth = 0
    if not usd:
        usd = 0
    isCarbonSaved = request.form.get('isCarbonSaved')
    bill = Bill()
    bill.desc = desc
    bill.ccChange = cc
    bill.usdChange = usd
    bill.ethChange = eth
    print(cc, usd, eth)
    score = abs(float(cc) * 1) + abs(float(usd) * 20) + abs(float(eth) * 10000)
    score = int(score)
    if isCarbonSaved == 'on':
        bill.carbonScore = str(score)
    db.session.add(bill)
    db.session.commit()
    print(session.get('user_id'))
    user = User.query.filter(User.id == session.get('user_id')).first()
    account = user.account[0]
    account.bills.append(bill)
    account.cc = str(float(cc)+float(account.cc))
    account.eth = str(float(eth)+float(account.eth))
    account.usd = str(float(usd)+float(account.usd))
    if float(account.eth) <= 0:
        account.eth = '0'
    if float(account.usd) <= 0:
        account.usd = '0'
    if float(account.cc) <= 0:
        account.cc = '0'
    db.session.commit()
    return redirect(url_for('bill'))


@app.route("/convert", methods=['GET','POST'])
@login_required
def convertETH():
    user = User.query.filter(User.id == session.get('user_id')).first()
    account = user.account[0]
    if account.cc>='100':
        cc=float(account.cc)
        cc-=100
        eth=float(account.eth)
        eth+=1
        account.cc=str(cc)
        account.eth=str(eth)
        db.session.commit()
        bill=Bill(desc="Convert CC to ETH",ccChange='-100',ethChange='+1')
        db.session.add(bill)
        db.session.commit()
        account.bills.append(bill)
        db.session.commit()
        return render_template('market.html',info='Convert Success')
    return render_template('market.html')


if __name__ == '__main__':
    app.run(debug=True)
